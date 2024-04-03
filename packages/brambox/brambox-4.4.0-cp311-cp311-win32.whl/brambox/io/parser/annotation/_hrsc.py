#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
import logging
import xml.etree.ElementTree as ET

from ._base import AnnotationParser, ParserType

__all__ = ['HRSCParser']
log = logging.getLogger(__name__)


class HRSCParser(AnnotationParser):
    """
    This parser can parse annotations in the `HRSC 2016 <hrsc_>`_ format.
    This format consists of one xml file for every image.

    Example:
        >>> image_100000001.xml
            <HRSC_Image>
              <Img_ID>100000001</Img_ID>
              <Place_ID>100000001</Place_ID>
              <Source_ID>100000001</Source_ID>
              <Img_NO>100000001</Img_NO>
              <Img_FileName>100000001</Img_FileName>
              <Img_FileFmt>bmp</Img_FileFmt>
              <Img_Date>2014-07-01</Img_Date>
              <Img_CusType>sealand</Img_CusType>
              <Img_Des></Img_Des>
              <Img_Location>69.040297,33.070036</Img_Location>
              <Img_SizeWidth>1166</Img_SizeWidth>
              <Img_SizeHeight>753</Img_SizeHeight>
              <Img_SizeDepth>3</Img_SizeDepth>
              <Img_Resolution>1.07</Img_Resolution>
              <Img_Resolution_Layer>18</Img_Resolution_Layer>
              <Img_Scale>100</Img_Scale>
              <Img_SclPxlNum></Img_SclPxlNum>
              <segmented>0</segmented>
              <Img_Havemask>0</Img_Havemask>
              <Img_MaskFileName></Img_MaskFileName>
              <Img_MaskFileFmt></Img_MaskFileFmt>
              <Img_MaskType></Img_MaskType>
              <Img_SegFileName></Img_SegFileName>
              <Img_SegFileFmt></Img_SegFileFmt>
              <Img_Rotation>090d</Img_Rotation>
              <Annotated>1</Annotated>
              <HRSC_Objects>
                <HRSC_Object>
                  <Object_ID>100000001</Object_ID>
                  <Class_ID>100000013</Class_ID>
                  <Object_NO>100000001</Object_NO>
                  <truncated>0</truncated>
                  <difficult>0</difficult>
                  <box_xmin>194</box_xmin>
                  <box_ymin>243</box_ymin>
                  <box_xmax>972</box_xmax>
                  <box_ymax>507</box_ymax>
                  <mbox_cx>582.9349</mbox_cx>
                  <mbox_cy>353.2006</mbox_cy>
                  <mbox_w>778.1303</mbox_w>
                  <mbox_h>174.2541</mbox_h>
                  <mbox_ang>-0.2144308</mbox_ang>
                  <segmented>0</segmented>
                  <seg_color></seg_color>
                  <header_x>964</header_x>
                  <header_y>290</header_y>
                </HRSC_Object>
              </HRSC_Objects>
            </HRSC_Image>
    """

    parser_type = ParserType.MULTI_FILE
    serialize_group = 'image'
    extension = '.xml'

    def __init__(self):
        super().__init__()
        log.warning('We only extract HBB information from this format. Extracting oriented data is possible, but not yet implemented.')

    def serialize(self, df):
        raise NotImplementedError('Serialization not implemented for this parser')

    def deserialize(self, rawdata, file_id=None):
        self.append_image(file_id)

        root = ET.fromstring(rawdata)
        for xml_obj in root.iter('HRSC_Object'):
            x_top_left = float(xml_obj.findtext('box_xmin', 0))
            y_top_left = float(xml_obj.findtext('box_ymin', 0))
            width = float(xml_obj.findtext('box_xmax', 0)) - x_top_left
            height = float(xml_obj.findtext('box_ymax', 0)) - y_top_left

            self.append(
                file_id,
                class_label=xml_obj.findtext('Class_ID', ''),
                x_top_left=x_top_left,
                y_top_left=y_top_left,
                width=width,
                height=height,
                truncated=float(xml_obj.findtext('truncated', 0)),
                occluded=float(xml_obj.findtext('occluded', 0)),
                difficult=xml_obj.findtext('difficult', 0) == '1',
            )
