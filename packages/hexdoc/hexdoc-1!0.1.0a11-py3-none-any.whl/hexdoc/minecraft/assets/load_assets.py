import base64
import logging
from collections.abc import Set
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any, Iterable, Iterator, TypeVar, cast

from minecraft_render import ResourcePath, js
from minecraft_render.types.dataset.RenderClass import IRenderClass
from minecraft_render.types.dataset.types import IResourceLoader
from pydantic import TypeAdapter
from yarl import URL

from hexdoc.core import ModResourceLoader, ResourceLocation
from hexdoc.core.properties import (
    PNGTextureOverride,
    TextureTextureOverride,
)
from hexdoc.model import HexdocModel
from hexdoc.utils import PydanticURL
from hexdoc.utils.context import ContextSource

from ..tags import Tag
from .animated import AnimatedTexture, AnimationMeta
from .constants import MISSING_TEXTURE_URL
from .items import (
    ImageTexture,
    ItemTexture,
    MultiItemTexture,
    SingleItemTexture,
)
from .models import FoundNormalTexture, ModelItem
from .textures import PNGTexture

logger = logging.getLogger(__name__)

Texture = ImageTexture | ItemTexture

_T_Texture = TypeVar("_T_Texture", bound=Texture)


def validate_texture(
    value: Any,
    *,
    context: ContextSource,
    model_type: type[_T_Texture] = Texture,
) -> _T_Texture:
    ta = TypeAdapter(model_type)
    return ta.validate_python(
        value,
        context=cast(dict[str, Any], context),  # lie
    )


class TextureNotFoundError(FileNotFoundError):
    def __init__(self, id_type: str, id: ResourceLocation):
        self.message = f"No texture found for {id_type} id: {id}"
        super().__init__(self.message)


class HexdocPythonResourceLoader(HexdocModel):
    loader: ModResourceLoader

    def loadJSON(self, resource_path: ResourcePath) -> str:
        path = self._convert_resource_path(resource_path)
        _, json_str = self.loader.load_resource(path, decode=lambda v: v)
        return json_str

    def loadTexture(self, resource_path: ResourcePath) -> str:
        path = self._convert_resource_path(resource_path)
        _, resolved_path = self.loader.find_resource(path)

        with open(resolved_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    def close(self):
        pass

    def wrapped(self):
        return js.PythonLoaderWrapper(self)

    def _convert_resource_path(self, resource_path: ResourcePath):
        string_path = js.resourcePathAsString(resource_path)
        return Path("assets") / string_path


@dataclass(kw_only=True)
class HexdocAssetLoader:
    loader: ModResourceLoader
    site_url: PydanticURL
    asset_url: PydanticURL
    render_dir: Path

    @cached_property
    def gaslighting_items(self):
        return Tag.GASLIGHTING_ITEMS.load(self.loader).value_ids_set

    def can_be_missing(self, id: ResourceLocation):
        return any(id.match(pattern) for pattern in self.loader.props.textures.missing)

    def get_override(
        self,
        id: ResourceLocation,
        image_textures: dict[ResourceLocation, ImageTexture],
    ) -> Texture | None:
        match self.loader.props.textures.override.get(id):
            case PNGTextureOverride(url=url, pixelated=pixelated):
                return PNGTexture(url=url, pixelated=pixelated)
            case TextureTextureOverride(texture=texture):
                return image_textures[texture]
            case None:
                return None

    def find_image_textures(
        self,
    ) -> Iterable[tuple[ResourceLocation, Path | ImageTexture]]:
        for resource_dir, texture_id, path in self.loader.find_resources(
            "assets",
            namespace="*",
            folder="textures",
            glob="**/*.png",
            internal_only=True,
            allow_missing=True,
        ):
            if resource_dir:
                self.loader.export_raw(
                    path=path.relative_to(resource_dir.path),
                    data=path.read_bytes(),
                )
            yield texture_id, path

    def load_item_models(self) -> Iterable[tuple[ResourceLocation, ModelItem]]:
        for _, item_id, data in self.loader.load_resources(
            "assets",
            namespace="*",
            folder="models/item",
            internal_only=True,
            allow_missing=True,
        ):
            model = ModelItem.load_data("item" / item_id, data)
            yield item_id, model

    def load_blockstates(self) -> Iterable[ResourceLocation]:
        for _, block_id, _ in self.loader.load_resources(
            "assets",
            namespace="*",
            folder="blockstates",
            internal_only=True,
            allow_missing=True,
        ):
            yield block_id

    @cached_property
    def renderer(self):
        self.render_dir.mkdir(parents=True, exist_ok=True)
        return js.RenderClass(
            self.renderer_loader(),
            {
                "outDir": self.render_dir.as_posix(),
                "imageSize": 300,
            },
        )

    def renderer_loader(self) -> IResourceLoader:
        return HexdocPythonResourceLoader(loader=self.loader).wrapped()

    def fallback_texture(self, item_id: ResourceLocation) -> ItemTexture | None:
        return None

    def load_and_render_internal_textures(
        self,
        image_textures: dict[ResourceLocation, ImageTexture],
    ) -> Iterator[tuple[ResourceLocation, Texture]]:
        """For all item/block models in all internal resource dirs, yields the item id
        (eg. `hexcasting:focus`) and some kind of texture that we can use in the book."""

        # images
        for texture_id, value in self.find_image_textures():
            if not texture_id.path.startswith("textures"):
                texture_id = "textures" / texture_id

            match value:
                case Path() as path:
                    texture = load_texture(
                        texture_id,
                        path=path,
                        repo_root=self.loader.props.repo_root,
                        asset_url=self.asset_url,
                    )

                case PNGTexture() | AnimatedTexture() as texture:
                    pass

            image_textures[texture_id] = texture
            yield texture_id, texture

        found_items_from_models = set[ResourceLocation]()
        missing_items = set[ResourceLocation]()

        missing_item_texture = SingleItemTexture.from_url(
            MISSING_TEXTURE_URL, pixelated=True
        )

        # items
        for item_id, model in self.load_item_models():
            if result := self.get_override(item_id, image_textures):
                yield item_id, result
            elif result := load_and_render_item(
                model,
                self.loader,
                self.renderer,
                self.gaslighting_items,
                image_textures,
                self.site_url,
            ):
                found_items_from_models.add(item_id)
                yield item_id, result
            else:
                missing_items.add(item_id)

        # blocks that didn't get covered by the items
        for block_id in self.load_blockstates():
            if block_id not in missing_items:
                continue

            try:
                yield block_id, render_block(block_id, self.renderer, self.site_url)
            except TextureNotFoundError:
                pass
            else:
                missing_items.remove(block_id)

        for item_id in list(missing_items):
            if result := self.fallback_texture(item_id):
                logger.warning(f"Using fallback texture for item: {item_id}")
            elif self.can_be_missing(item_id):
                logger.warning(f"Using missing texture for item: {item_id}")
                result = missing_item_texture
            else:
                continue
            missing_items.remove(item_id)
            yield item_id, result

        # oopsies
        if missing_items:
            raise FileNotFoundError(
                "Failed to find a texture for some items: "
                + ", ".join(str(item) for item in missing_items)
            )


def load_texture(
    id: ResourceLocation,
    *,
    path: Path,
    repo_root: Path,
    asset_url: URL,
) -> ImageTexture:
    url = asset_url.joinpath(*path.relative_to(repo_root).parts)
    meta_path = path.with_suffix(".png.mcmeta")

    if meta_path.is_file():
        try:
            meta = AnimationMeta.model_validate_json(meta_path.read_bytes())
        except ValueError as e:
            logger.debug(f"Failed to parse AnimationMeta for {id}\n{e}")
        else:
            return AnimatedTexture(
                url=url,
                pixelated=True,
                css_class=id.css_class,
                meta=meta,
            )

    return PNGTexture(url=url, pixelated=True)


def load_and_render_item(
    model: ModelItem,
    loader: ModResourceLoader,
    renderer: IRenderClass,
    gaslighting_items: Set[ResourceLocation],
    image_textures: dict[ResourceLocation, ImageTexture],
    site_url: URL,
) -> ItemTexture | None:
    try:
        match model.find_texture(loader, gaslighting_items):
            case None:
                return None

            case "gaslighting", found_textures:
                textures = list(
                    lookup_or_render_single_item(
                        found_texture,
                        renderer,
                        image_textures,
                        site_url,
                    ).inner
                    for found_texture in found_textures
                )
                return MultiItemTexture(inner=textures, gaslighting=True)

            case found_texture:
                texture = lookup_or_render_single_item(
                    found_texture,
                    renderer,
                    image_textures,
                    site_url,
                )
                return texture
    except TextureNotFoundError as e:
        logger.warning(e.message)
        return None


# TODO: move to methods on a class returned by find_texture?
def lookup_or_render_single_item(
    found_texture: FoundNormalTexture,
    renderer: IRenderClass,
    image_textures: dict[ResourceLocation, ImageTexture],
    site_url: URL,
) -> SingleItemTexture:
    match found_texture:
        case "texture", texture_id:
            if texture_id not in image_textures:
                raise TextureNotFoundError("item", texture_id)
            return SingleItemTexture(inner=image_textures[texture_id])

        case "block_model", model_id:
            return render_block(model_id, renderer, site_url)


def render_block(
    id: ResourceLocation,
    renderer: IRenderClass,
    site_url: URL,
) -> SingleItemTexture:
    render_id = js.ResourceLocation(id.namespace, id.path)
    file_id = id + ".png"

    if file_id.path.startswith("block/"):
        # model
        result = renderer.renderToFile(render_id)
    else:
        # blockstate
        file_id = "block" / file_id
        result = renderer.renderToFile(render_id, file_id.path)

    if not result:
        raise TextureNotFoundError("block", id)

    out_root, out_path = result

    # blocks look better if antialiased
    logger.debug(f"Rendered {id} to {out_path} (in {out_root})")

    # TODO: ideally we shouldn't be using site_url here, in case the site is moved
    # but I'm not sure what else we could do...
    return SingleItemTexture.from_url(site_url / out_path, pixelated=False)
