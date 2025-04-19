import xml.etree.ElementTree as ET
from Agents.logg.logger import logger
def parse(xml,agent="Agent"):
    try:
        parsed_xml = xml_parser(xml)
        logger.info(f"{agent} -- Parsing Successfull")
       
        return parsed_xml
    except Exception as e:
        logger.warning(f"{agent} -- The LLm has produced non parsable xml")
        logger.debug(f"{agent} -- Non Parsable XML == >{xml}")
        logger.debug(f"{agent} -- Parsing Error ==> {e}")
        return """THE RESULT YOU HAVE PROVIDED IS UNABLE TO PARSE.KINDLY FOLLOW THE CORRECT SYNTAX# Reminder: Instructions for Tool Use

        Tool uses are formatted using XML-style tags. The tool name is enclosed in opening and closing tags, and each parameter is similarly enclosed within its own set of tags. Here's the structure:

        <tool_name>
        <parameter1_name>value1</parameter1_name>
        <parameter2_name>value2</parameter2_name>
        ...
        </tool_name>

        For example:

        <plan_mode_respond>
        <response><![CDATA[Your response here]]></response>
        <options>
        <![CDATA[Set of options here (optional), e.g. Option 1 , Option 2 , Option 3.]]>
        </options>
        </plan_mode_respond>

        Always adhere to this format for all tool uses to ensure proper parsing and execution."""


def xml_parser(xml_string: str) -> dict:
    from lxml import etree
    
    def xml_to_dict(elem):
        children = list(elem)
        if not children:
            return elem.text.strip() if elem.text else None
        result = {}
        for child in children:
            tag = child.tag
            child_dict = xml_to_dict(child)
            if tag in result:
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(child_dict)
            else:
                result[tag] = child_dict
        return result
    

    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(f"<root>{xml_string}</root>", parser=parser)
    return {child.tag: xml_to_dict(child) for child in root}


