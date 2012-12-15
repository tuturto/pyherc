import os
from xml.dom.minidom import parse, parseString

def write_header(f):    
    f.write('<html>\n')
    f.write('<head><title>Test results</title></head>\n')
    f.write('<body>\n')

def write_summary(f, test_caption, top_element):
    
    f.write('<tr>\n')
    f.write('<th colspan="4" align="left"><h2>{0}</h2></th>\n'.format(
                                    test_caption))
    f.write('</tr>\n')
    f.write('<th colspan="4">Tests: {0}, Errors: {1}, Failures: {2}, Skip: {3}</th>\n'.format(
                                    top_element.getAttribute('tests'),
                                    top_element.getAttribute('errors'),
                                    top_element.getAttribute('failures'),
                                    top_element.getAttribute('skip')))
    f.write('</tr>\n')

def write_results(f, top_element):
    cases = top_element.getElementsByTagName('testcase')
    sorted_cases = {}
    for case in cases:
        class_name = case.getAttribute('classname')
        if sorted_cases.has_key(class_name):
            sorted_cases[class_name].append(case)
        else:
            sorted_cases[class_name] = [case]
    
    class_names = sorted_cases.keys()
    
    f.write('<tr>')
    f.write('<th align="left">Test class</th><th align="left">Test case</th><th align="left">Result</th><th align="left">Time</th>')
    f.write('</tr>')
    
    for class_name in class_names:
        test_case = sorted_cases[class_name]
        f.write('<tr>\n')
        f.write('<td>{0}</td>\n'.format(class_name))
        for case in test_case:
            f.write('<tr>\n')
            failure = case.getElementsByTagName('failure')
            error = case.getElementsByTagName('error')
            if len(error) > 0:
                f.write('<td></td><td>{0}</td><td>Error</td><td>{1}</td>\n'.format(
                                        case.getAttribute('name'),
                                        case.getAttribute('time')))            
            elif len(failure) > 0:
                f.write('<td></td><td>{0}</td><td>Failure</td><td>{1}</td>\n'.format(
                                        case.getAttribute('name'),
                                        case.getAttribute('time')))
            else:
                f.write('<td></td><td>{0}</td><td>Ok</td><td>{1}</td>\n'.format(
                                        case.getAttribute('name'),
                                        case.getAttribute('time')))
            
def write_test_suite(xunit_file_name, caption, report_file_name):    
    document = parse(xunit_file_name)
    top_element = document.documentElement
    write_summary(report_file_name, caption, top_element)
    write_results(report_file_name, top_element)

f = open('doc/test_results.html', 'w')
write_header(f)
f.write('<table border="0">\n')

files = os.listdir('./doc/behave/reports/')
for file in files:
    #caption = 'TESTS-combat.xml'
    caption = file
    dash_location = caption.find('-')
    caption = caption[dash_location+1:-4]
    caption = caption.capitalize()
    
    write_test_suite(os.path.join('./doc/behave/reports/', file), caption, f)

write_test_suite('nosetests.xml', 'Unit tests', f)

f.write('</tr>\n')
f.close()
