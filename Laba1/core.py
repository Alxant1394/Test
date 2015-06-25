from PlayListCreate import PlayListCreator
import time

__author__ = 'alxant'


def main():
    config_file = open('run.conf', "r")
    param = config_file.readline()
    depth = config_file.readline()
    genre = config_file.readline()

    print 'Gevent mod: ', param, 'Depth: ', depth, 'Genre: ', genre

    scrappy = PlayListCreator(input_path='Start.xml', output_path='out.xml',
                              given_depth=depth, genre=genre)
    urls = scrappy.get_url_from_xml()
    tags = scrappy.get_tags_from_xml()

    if param == 'gevent\n':
        scrappy.multitask_scrapper(urls)
        scrappy.write_xml()
    elif param == 'non-gevent\n':
        for url in urls:
            scrappy.scrapper(url)
        scrappy.write_xml()
    else:
        raise RuntimeError("RuntimeError")


start_time = time.time()
main()
print '--- %s seconds ---' % (time.time() - start_time)
