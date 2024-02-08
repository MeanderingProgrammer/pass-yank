from yank import MetadataValue, get_first, parse_metadata


def test_full() -> None:
    lines: list[str] = [
        "super-secret-password",
        "Username: user@example.com",
        "User Id: my-user-id",
        "url: *.amazon.com/*",
        "URL: https://amazon.com/some-url",
    ]
    actual_metadata = parse_metadata(lines)
    expected_metadata = dict(
        username=MetadataValue(key="Username", value="user@example.com"),
        user_id=MetadataValue(key="User Id", value="my-user-id"),
        url=MetadataValue(key="url", value="*.amazon.com/*"),
    )
    assert expected_metadata == actual_metadata

    actual_default = get_first(actual_metadata, ["^user.*$", "^email.*$"])
    assert expected_metadata["username"] == actual_default

    actual_url = get_first(actual_metadata, ["url"])
    assert expected_metadata["url"] == actual_url

    assert get_first(actual_metadata, ["amazon"]) is None
