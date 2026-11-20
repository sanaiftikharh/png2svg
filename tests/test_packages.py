def test_public_api_is_available():
    from png2svg import PNGToSVGConverter, convert_image_to_svg

    assert callable(convert_image_to_svg)
    assert PNGToSVGConverter is not None