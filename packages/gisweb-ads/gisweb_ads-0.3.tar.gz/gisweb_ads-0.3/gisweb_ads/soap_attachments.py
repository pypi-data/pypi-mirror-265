# -*- coding: utf-8 -*-
import uuid
import logging
import xml.etree.ElementTree as ET
from gisweb_ads.schema import IResult

_logger = logging.getLogger('gisweb.sicraweb')

def parseMessage(xmlMessage) -> IResult:

  root = ET.fromstring(xmlMessage)
  ret = IResult(lngErrNumber=666, strErrString='Errore nel parser del risultato')
  if len(root[0])==2:
    result = root[0][1]
  else:
    result = root[0][0][0]

  for node in result:
    if 'lngDocID' in node.tag:
      ret.lngDocID = int(node.text or '0')
    if 'lngErrNumber' in node.tag:
      ret.lngErrNumber = int(node.text or '0')
    if 'strErrString' in node.tag:
      ret.strErrString = node.text or ''
    if 'lngNumPG' in node.tag:
      ret.lngNumPG = int(node.text or '0')
    if 'lngAnnoPG' in node.tag:
      ret.lngAnnoPG = int(node.text or '0')
    if 'strDataPG' in node.tag:
      ret.strDataPG = node.text or ''
      
    if ret.lngErrNumber == 0:
      ret.strErrString = ''
      
  return ret



def with_soap_attachment(suds_method, attachment_data, *args, **kwargs) -> IResult:
    """ Add an attachment to a suds soap request.

    attachment_data is assumed to contain a list:
      ( <attachment content>, <content id>, <mime-type> )

    The attachment content is only required required list element.

    http://stackoverflow.com/questions/17046779/passing-file-attachments-in-soap-using-suds

    """

    from suds.transport import Request

    # Suds doesn't currently support SOAP Attachments, so we have to build our
    # own attachment support, using parts of the suds library

    MIME_DEFAULT = 'text/plain'
    attachment_encoding = '8bit'
    attachment_mimetype = MIME_DEFAULT
    attachment_id = ''
    soap_method = suds_method.method
    data: bytes
    
        
    if len(attachment_data) == 3:
        data, attachment_id, attachment_mimetype = attachment_data
    elif len(attachment_data) == 2:
        data, attachment_id = attachment_data
    elif len(attachment_data) == 1:
        data = attachment_data
        attachment_id = uuid.uuid4()

    # Generate SOAP XML appropriate for this request
    binding = soap_method.binding.input
    soap_xml = binding.get_message(soap_method, args, kwargs).str().encode('utf-8')
    
    # Prepare MIME headers & boundaries
    boundary_id = f'uuid:{uuid.uuid4()}'
    root_part_id = f'uuid:{uuid.uuid4()}'
    request_headers = {
      'Content-Type': '; '.join([
          'multipart/related',
          'type="text/xml"',
          f'start="<{root_part_id}>"',
          f'boundary="{boundary_id}"',
        ]),
      'SOAPAction':''
    }
    soap_headers = '\n'.join([
      'Content-Type: text/xml; charset=UTF-8',
      'Content-Transfer-Encoding: 8bit',
      f'Content-Id: <{root_part_id}>',
      '',
    ]).encode('utf-8')
    attachment_headers = '\n'.join([
      f'Content-Type: {attachment_mimetype}',
      f'Content-Transfer-Encoding: {attachment_encoding}',
      f'Content-Id: <{attachment_id}>',
      '',
    ]).encode('utf-8')
    
    boundary = f"--{boundary_id}".encode('utf-8')

    # Build the full request
    request_text = b'\r\n'.join([
      boundary,
      soap_headers,
      soap_xml,
      boundary,
      attachment_headers,
      data,
      boundary + '--'.encode('utf-8')
    ])
    
    #with open("./test.xml", "w") as f:
    #  f.write(request_text.decode('latin-1'))

    # Stuff everything into a request object
    headers = suds_method.client.options.headers.copy()
    headers.update(request_headers)
    request = Request(suds_method.client.wsdl.url, request_text)
    request.headers = headers
    # Send the request
    #_logger.info(request_text)
    

    response = suds_method.client.options.transport.send(request)
    if response.code==200:
      return parseMessage(response.message)
    else:
      return IResult(lngErrNumber=999, strErrString= "ERRORE NELLA RISPOSTA DEL SERVIZIO")

