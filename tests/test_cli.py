from document_ocr.cli.main import create_parser


def test_cli_defaults():

    parser = create_parser()

    args = parser.parse_args(["sample.png"])

    assert str(args.input) == "sample.png"
    assert args.language == "eng"
    assert args.format == "both"
    assert args.dpi == 200
    assert args.max_pages is None


def test_cli_options():

    parser = create_parser()

    args = parser.parse_args(
        [
            "sample.pdf",
            "--language",
            "hin+eng",
            "--format",
            "json",
            "--dpi",
            "300",
            "--max-pages",
            "10",
        ]
    )

    assert args.language == "hin+eng"
    assert args.format == "json"
    assert args.dpi == 300
    assert args.max_pages == 10
