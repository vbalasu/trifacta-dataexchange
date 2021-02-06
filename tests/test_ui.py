# Make sure `chalice local` is running
def test_example(selenium):
    selenium.implicitly_wait(2) # seconds
    selenium.get('http://127.0.0.1:8000')
    logo = selenium.find_element_by_id("trifactalogo")
    assert logo is not None
    heading = selenium.find_element_by_id('heading').get_attribute('innerHTML')
    assert heading == 'AWS Data Exchange - Import Data'
    import time
    time.sleep(2)
