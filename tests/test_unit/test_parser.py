import pytest

from ncoreparser.parser import ActivityParser, TorrentActivity
from ncoreparser.util import Size


@pytest.fixture
def parser():
    return ActivityParser()

@pytest.fixture
def sample_html():
    return """
    <div class="hnr_torrents">
        <div class="hnr_all2">
            <div class="hnr_tname">
                <a onclick="torrent(1111111);" title="Mock.Movie.One.2024.1080p.BluRay.x264-TESTER"><nobr>Mock.Movie.One.2024.1080p.BluRay.x264-TESTER</nobr></a>
            </div>
            <div class="hnr_tstart">5 napja</div>
            <div class="hnr_tlastactive">10 perce</div>
            <div class="hnr_tseed"><span class="stopped">Seed</span></div>
            <div class="hnr_tup">0 B</div>
            <div class="hnr_tdown">5.50 GiB</div>
            <div class="hnr_ttimespent"><span class="stopped">12ó 30p</span></div>
            <div class="hnr_tratio"><span class="stopped">0.000</span></div>
        </div>
    </div>
    <div class="hnr_torrents">
        <div class="hnr_all">
            <div class="hnr_tname">
                <a onclick="torrent(9999999);" title="Example.Show.S01E01.720p.WEB.H264-RANDOM"><nobr>Example.Show.S01E01.720p...</nobr></a>
            </div>
            <div class="hnr_tstart">1 napja</div>
            <div class="hnr_tlastactive">5 perce</div>
            <div class="hnr_tseed"><span class="stopped">Seed</span></div>
            <div class="hnr_tup">2.5 GiB</div>
            <div class="hnr_tdown">10.0 GiB</div>
            <div class="hnr_ttimespent"><span class="stopped">48ó 00p</span></div>
            <div class="hnr_tratio"><span class="stopped">0.250</span></div>
        </div>
    </div>
    """

def test_activity_parser_returns_empty_list_when_no_torrents_in_html(parser):
    # Given
    empty_html = "<html><body><div class='hnr_torrents'></div></body></html>"

    # When
    result = parser.parse(empty_html)

    # Then
    assert result == []
    assert len(result) == 0

def test_parse_returns_correct_count(parser, sample_html):
    results = parser.parse(sample_html)
    assert len(results) == 2

@pytest.mark.parametrize("index, expected", [
    (0, TorrentActivity(
            torrent_id="1111111",
            torrent_title="Mock.Movie.One.2024.1080p.BluRay.x264-TESTER",
            start="5 napja",
            updated="10 perce",
            status=TorrentActivity.Status.SEEDING,
            uploaded=Size("0 B"),
            downloaded=Size("5.50 GiB"),
            remaining="12ó 30p",
            ratio=0.0
        )
    ),
    (1, TorrentActivity(
            torrent_id="9999999",
            torrent_title="Example.Show.S01E01.720p.WEB.H264-RANDOM",
            start="1 napja",
            updated="5 perce",
            status=TorrentActivity.Status.SEEDING,
            uploaded=Size("2.5 GiB"),
            downloaded=Size("10.0 GiB"),
            remaining="48ó 00p",
            ratio=0.250
        )
    ),
])
def test_parse_item_details(parser, sample_html, index, expected):
    results = parser.parse(sample_html)
    item = results[index]
    
    assert isinstance(item, TorrentActivity)
    
    assert item == expected
