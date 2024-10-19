import pytest
from downloader import download_audio_and_metadata

def test_downloader_audio():
    url1 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result1 = download_audio_and_metadata(url1)
    expected_result1 = (
        'Rick Astley  Never Gonna Give You Up Official Music Video.mp3',
        'thumbnail.jpg',
        'Rick Astley - Never Gonna Give You Up (Official Music Video)',
        'Rick Astley',
        'Rick Astley - Never Gonna Give You Up (Official Music Video)',
        'Rick Astley',
        '2009',
        '')
    assert result1 == expected_result1

    url2 = "https://www.youtube.com/watch?v=cLXQnnVWJGo"
    result2 = download_audio_and_metadata(url2)
    expected_result2 = (
        'Sorting Pebbles Into Correct Heaps  A Short Story By Eliezer Yudkowsky.mp3',
        'thumbnail.jpg',
        'Sorting Pebbles Into Correct Heaps - A Short Story By Eliezer Yudkowsky',
        'Rational Animations',
        'Sorting Pebbles Into Correct Heaps - A Short Story By Eliezer Yudkowsky',
        'Rational Animations',
        '2023',
        '')
    assert result2 == expected_result2

    url3 = "https://music.youtube.com/watch?v=VwSEH3GY7TU"
    result3 = download_audio_and_metadata(url3)
    expected_result3 = (
        'Charter Cities.mp3',
        'thumbnail.jpg',
        'Charter Cities',
        'Epic Mountain - Topic',
        'Charter Cities',
        'Epic Mountain - Topic',
        '2024',
        '')
    assert result3 == expected_result3