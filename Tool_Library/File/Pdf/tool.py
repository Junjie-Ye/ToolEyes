from pylovepdf.tools.compress import Compress
from pylovepdf.tools.imagetopdf import ImageToPdf
from pylovepdf.tools.merge import Merge
from pylovepdf.tools.officepdf import OfficeToPdf
from pylovepdf.tools.pagenumber import Pagenumber
from pylovepdf.tools.pdftojpg import PdfToJpg
from pylovepdf.tools.protect import Protect
from pylovepdf.tools.rotate import Rotate
from pylovepdf.tools.split import Split
from pylovepdf.tools.unlock import Unlock
from pylovepdf.tools.watermark import Watermark

'''
pylovepdf库的output_filename似乎有些问题, 输出的文件名可能与指定有所不同
'''


def process(t, file_path: str, output_dir: str, output_filename: str):
    t.add_file(file_path=file_path)
    t.set_output_folder(output_dir)
    if output_filename is not None:
        t.output_filename = f'file_{output_filename}'
    t.execute()
    t.download()
    t.delete_current_task()


def compress(file_path: str, output_filename=None, output_dir: str = './output_dir', public_key: str = ''):
    try:
        t = Compress(public_key, verify_ssl=True, proxies=None)
        process(t, file_path, output_dir, output_filename)
        return {"success": "process successfully."}
    except:
        return {"error": "an error occurred."}


def image_to_pdf(img_path: str, output_filename=None,  output_dir: str = './output_dir', public_key: str = ''):
    try:
        t = ImageToPdf(public_key, verify_ssl=True, proxies=None)
        process(t, img_path, output_dir, output_filename)
        return {"success": "process successfully."}
    except Exception as e:
        return {"error": e}


def merge(file_path: list[str], output_filename=None, output_dir: str = './output_dir', public_key: str = ''):
    try:
        t = Merge(public_key, verify_ssl=True, proxies=None)
        for file in file_path:
            t.add_file(file)
        t.set_output_folder(output_dir)
        if output_filename is not None:
            t.output_filename = f'file_{output_filename}'
        t.execute()
        t.download()
        t.delete_current_task()
        return {"success": "process successfully."}
    except Exception as e:
        return {"error": e}


def office_to_pdf(file_path: str, output_filename: str = None, output_dir: str = './output_dir', public_key: str = ''):
    try:
        t = OfficeToPdf(public_key, verify_ssl=True, proxies=None)
        process(t, file_path, output_dir, output_filename)
        return {"success": "process successfully."}
    except:
        return {"error": "an error occurred."}


def add_page_number(file_path: str, output_filename: str = None, output_dir: str = './output_dir', public_key: str = ''):
    try:
        t = Pagenumber(public_key, verify_ssl=True, proxies=None)
        process(t, file_path, output_dir, output_filename)
        return {"success": "process successfully."}
    except Exception as e:
        return {"error": e}


def pdf_to_img(file_path: str, output_filename: str = None, output_dir: str = './output_dir', public_key: str = ''):
    try:
        t = PdfToJpg(public_key, verify_ssl=True, proxies=None)
        process(t, file_path, output_dir, output_filename)
        return {"success": "process successfully."}
    except Exception as e:
        return {"error": e}


def add_password(file_path: str, password: str = '123456', output_filename: str = None, output_dir: str = './output_dir/', public_key: str = ''):
    try:
        t = Protect(public_key, verify_ssl=True, proxies=None)
        t.add_file(file_path)
        t.file.password = password
        t.set_output_folder(output_dir)
        if output_filename is not None:
            t.output_filename = f'file_{output_filename}'
        t.execute()
        t.download()
        t.delete_current_task()
        return {"success": "process successfully."}
    except Exception as e:
        return {"error": e}


def rotate(file_path: str, angle: int, output_filename: str = None, output_dir: str = './output_dir', public_key: str = ''):
    try:
        t = Rotate(public_key, verify_ssl=True, proxies=None)
        t.add_file(file_path)
        t.file.rotate = angle
        t.set_output_folder(output_dir)
        if output_filename is not None:
            t.output_filename = f'file_{output_filename}'
        t.execute()
        t.download()
        t.delete_current_task()
        return {"success": "process successfully."}
    except Exception as e:
        return {"error": e}


def split(file_path: str, output_dir: str = './output_dir', split_mode='fixed_range', public_key: str = '', **kargs):
    try:
        t = Split(public_key, verify_ssl=True, proxies=None)
        t.add_file(file_path)
        t.set_output_folder(output_dir)
        t.split_mode = split_mode
        if split_mode == 'fixed_range':
            t.fixed_range = kargs['fixed_range']
        elif split_mode == 'ranges':
            t.ranges = kargs['ranges']
        elif split_mode == 'remove_pages':
            t.remove_pages = kargs['remove_pages']
        else:
            return {"error": "Unsupported split_mode."}
        t.execute()
        t.download()
        t.delete_current_task()
        return {"success": "process successfully."}
    except Exception as e:
        return {"error": e}


def unlock(file_path: str, output_filename: str = None, output_dir: str = './output_dir', public_key: str = ''):
    try:
        t = Unlock(public_key, verify_ssl=True, proxies=None)
        process(t, file_path, output_dir, output_filename)
        return {"success": "process successfully."}
    except Exception as e:
        return {"error": e}


def add_watermark(file_path: str, text: str, output_filename: str = None, output_dir: str = './output_dir', public_key: str = ''):
    try:
        t = Watermark(public_key, verify_ssl=True, proxies=None)
        t.mode = 'text'
        t.text = text
        process(t, file_path, output_dir, output_filename)
        return {"success": "process successfully."}
    except Exception as e:
        return {"error", e}


if __name__ == '__main__':
    # print(compress('./test_file/hello.pdf', 'compress.pdf'))
    # print(image_to_pdf('./test_file/hello.png', 'image.pdf'))
    # print(merge(['./test_file/hello.pdf', './test_file/world.pdf'], 'merge.pdf'))
    # print(office_to_pdf('./test_file/hello.doc', 'office.pdf'))
    # print(add_page_number('./test_file/hello.pdf', 'pagenumber.pdf'))
    # print(pdf_to_img('./test_file/hello.pdf'))
    # print(add_password('./test_file/hello.pdf', 'password.pdf'))
    # print(rotate('./test_file/hello.pdf', 90, 'rotate.pdf'))
    # print(split('./test_file/merge.pdf', fixed_range='1'))
    # print(split('./test_file/merge.pdf', split_mode='ranges', ranges='1,2'))
    print(unlock('/workspace/Tool_learning_test/Tools/File/Pdf/test_file/protect.pdf',
          'unlock.pdf', '/workspace/Tool_learning_test/Tools/File/Pdf/test_file/'))
    # print(add_watermark('./test_file/hello.pdf', 'hello, world!', 'watermark.pdf'))
    pass
