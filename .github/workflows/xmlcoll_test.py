import requests, io
import xmlcoll.coll as xc


def get_collection(xpath=""):
    coll = xc.Collection()
    coll.update_from_xml(
        io.BytesIO(requests.get("https://osf.io/k5c9m/download").content),
        xpath=xpath,
    )
    return coll


def test_load():
    coll = get_collection()
    assert coll.get_properties()["Title"] == "Famous Paintings"
    assert coll.get_properties()["Original Collator"] == "Brad Meyer"


def test_items():
    coll = get_collection()
    assert len(coll.get()) > 0


def test_item():
    coll = get_collection()
    items = coll.get()
    for item in items:
        assert item
        assert items[item]
        assert items[item].get_properties()


def test_xpath():
    coll = get_collection(
        xpath="[.//property[@tag1 = 'nationality'] = 'Dutch']"
    )
    assert len(coll.get()) > 0


def test_update_name():
    coll = get_collection()
    assert "Guernica" in coll.get()
    coll.update_item_name("Guernica", "Picasso's Guernica")
    assert "Guernica" not in coll.get() and "Picasso's Guernica" in coll.get()
    assert coll.get()["Picasso's Guernica"].get_name() == "Picasso's Guernica"


def test_write(tmpdir):
    coll = get_collection()
    file = tmpdir.join("out.xml")
    assert not coll.write_to_xml(str(file))
    assert not coll.validate(str(file))


def test_dataframe(tmpdir):
    coll = get_collection()
    df = coll.get_dataframe()
    file1 = tmpdir.join("out.xlsx")
    assert not df.to_excel(str(file1))
    df_new = df[["date", "artist_name_last"]]
    reduced_collection = xc.Collection()
    assert not reduced_collection.update_from_dataframe(df_new)
    file2 = tmpdir.join("out2.xml")
    assert not reduced_collection.write_to_xml(str(file2))

def test_properties():
    coll = get_collection()
    item = coll.get()['The Sleeping Gypsy'] 
    assert item.get_properties()['date'] == '1897'
    assert 'favorite' not in item.get_properties()
    item.update_properties({'date': '1896', 'favorite': 'true'})
    assert item.get_properties()['date'] == '1896'
    assert 'favorite' in item.get_properties()
    item.get_properties()['my favorite'] = item.get_properties().pop('favorite')
    assert 'favorite' not in item.get_properties()
    assert 'my favorite' in item.get_properties()
