#!/usr/bin/python3

""" Cheap Pie Module to export register descriptio into .docx file """

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from operator import attrgetter
from docx import Document
# from docx.enum.table import WD_TABLE_ALIGNMENT

from cheap_pie.cheap_pie_core.cbitfield import CpBitfield # pylint: disable=C0413,E0401

INCH2EMU = 914400

def reg_add_reserved_bitfields(fields,regwidth=32):
    """ Add inferred reserved bits to register description """
    next_lsb = 0
    outfields = []

    if isinstance(fields,list):
        if len(fields) > 0:
            for idx in reversed(range(len(fields))):
                field = fields[idx]
                outfields.insert(0,field)
                #outfields.append(field)

                if next_lsb < field.lsb:
                    # print("Add Reserved field!")
                    newfield=CpBitfield("Reserved",0,field.regname,
                                         field.lsb-next_lsb,next_lsb,"Reserved")
                    outfields.insert(1,newfield)
                    # outfields.append(newfield)

                # print("LSB: %d, WIDTH: %d" % ( field.lsb, field.width ) )
                next_lsb = field.lsb + field.width

            # check if register is filled up to full width
            if next_lsb < regwidth:
                newfield=CpBitfield("Reserved",0,fields[0].regname,
                                     regwidth-next_lsb,next_lsb,"Reserved")
                outfields.insert(0,newfield)

    return outfields

def int2hexstr(num,width): # pylint: disable=W0613
    """ Convert integer into hex string """
    fmt = "%%0%dx" % width          # pylint: disable=C0209
    # print fmt
    string = "\"%s\" %% num " % fmt # pylint: disable=C0209
    # print string
    return eval(string) # pylint: disable=W0123

def doc_create_header(template=None):
    """ Create document header """
    if template is None:
        document = Document()
    else :
        document = Document(template)

    # document.add_heading('Document Title', 0)
    document.add_heading('Register Description', level=1)
    document.add_paragraph("")

    return document

def doc_add_regtable(doc,reg,tablestyle=None,nbits_addr=32): # pylint: disable=R0912
    """ Add table description of a register to a document """
    # header
    doc.add_heading(reg.regname, level=3)

    # address
    doc.add_paragraph('Offset Address: 0x%s' % int2hexstr(reg.addr,nbits_addr/4)) # pylint: disable=C0209

    # description
    if isinstance(reg.comments,str):
        doc.add_paragraph(reg.comments)
    else:
        print("Warning: Non-string comments for reg: " + reg.regname)

    # bitfields table
    table = doc.add_table(rows=1, cols=5)

    if tablestyle is not None:
        table.style = tablestyle
    # table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # configure column width
    # https://stackoverflow.com/questions/43749177/python-docx-table-column-width
    # inch2emu = 914400
    cwidths = [         1.5,  0.5,    0.5,      1,            3]

    # create table header
    headers = ['Field name','rwu','Bit #','Reset','Description']
    hdr_cells = table.rows[0].cells

    for idx in range(len(headers)): # pylint: disable=C0200
        hdr_cells[idx].text  = headers[idx]
        hdr_cells[idx].width = cwidths[idx]*INCH2EMU
        hdr_cells[idx].bold  = True
        # hdr_cells[idx].alignment=WD_ALIGN_PARAGRAPH.CENTER

    # add bitfields
    for field in reversed(reg.bitfields):
        row_cells = table.add_row().cells
        row_cells[0].text = field.fieldname
        row_cells[0].width = cwidths[0]*INCH2EMU

        if len(field.read_write)/field.width > 1:
            row_cells[1].text = str.lower(field.read_write[0:2])
        else:
            row_cells[1].text = str.lower(field.read_write)
        row_cells[1].width = cwidths[1]*INCH2EMU

        if field.width == 1:
            row_cells[2].text = "%d" % ( field.lsb ) # pylint: disable=C0209
        else:
            row_cells[2].text = "%d:%d" % ( field.lsb + field.width -1, field.lsb) # pylint: disable=C0209
        row_cells[2].width = cwidths[2]*INCH2EMU

        if isinstance(field.reset,str):
            row_cells[3].text = field.reset
        else:
            resetstr = "%d\'%s" % (field.width, bin(field.reset)[1:]) # pylint: disable=C0209
            row_cells[3].text = resetstr
        row_cells[3].width = cwidths[3]*INCH2EMU

        if isinstance(reg.comments,str):
            row_cells[4].text = field.comments
            row_cells[4].width = cwidths[4]*INCH2EMU
            # print(field.comments)
        else:
            print(f"Warning: Non-string comments for field: \
                  {field.fieldname} in reg: {reg.regname}")

    doc.add_paragraph("")

def hal2doc(hal,fname='hal.docx',template=None,tablestyle=None,nbits_addr=32):
    """  export register description to .docx file """
    # initialize doc
    doc = doc_create_header(template)

    # loop over registers
    for reg in hal:
        # print(reg.regname)

        # convert bitfields namedtuple into list
        bitfields = list(reg.bitfields)

        # sort by lsb
        bitfields=sorted(bitfields,key=attrgetter('lsb'))
        bitfields.reverse()

        # add reserved bitfields
        reg.bitfields = reg_add_reserved_bitfields(bitfields)

        # create register table
        doc_add_regtable(doc,reg,tablestyle,nbits_addr)

    # save document
    doc.save(fname)

def test_hal2doc():
    """ Test function for export tool from register description to .docx """
    print('Testing hal2doc...')

    from cheap_pie.parsers.ipxact_parse import ipxact_parse      # pylint: disable=C0413,E0401,C0415
    from cheap_pie.cheap_pie_core.cp_cli import cp_devices_fname # pylint: disable=C0413,E0401,C0415

    fname = cp_devices_fname("my_subblock.xml")
    hal = ipxact_parse(fname=fname)

    # convert to .docx
    hal2doc(hal)

if __name__ == '__main__':
    test_hal2doc()
