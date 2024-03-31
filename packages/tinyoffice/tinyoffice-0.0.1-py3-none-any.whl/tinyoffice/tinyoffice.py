import enum
import io
import os
import tempfile
import zipfile

from collections import namedtuple
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from PIL import Image

try:
    from rich import print
except ModuleNotFoundError:
    pass


CompressionRecord = namedtuple(
    'CompressionRecord',
    [
        'filename',
        'errors',
        'num_images_compressed',
        'num_images_converted',
        'num_images_skipped',
        'start_size',
        'compressed_size',
    ]
)


class Verbosity(enum.Enum):
    NONE = enum.auto()
    LOW = enum.auto()
    NORMAL = enum.auto()
    HIGH = enum.auto()


def walk(
    cwd,
    *,
    types=None,
    overwrite=False,
    output=None,
    convert=False,
    verbosity=Verbosity.NORMAL,
    image_extensions=None,
):
    """
    Recursively iterates over the files in the directory
    and attempts to compress them if they match the listed file types

    Args:
        cwd: Path to directory to start from

    Kwargs:
        types: Office filetype extension(s) to use.
               Accepts either a str or list-like object.
               Default is None which will use .docx, .pptx, and .xlsx
        output: Location root to add save the compressed files.
                Default is None which will use the location where
                the script was called
        overwrite: Overwrite if output exists. Default is False
        convert: Convert TIFFs to JPEGs. Default is False
        verbosity: Verbosity level. Default is Verbosity.NORMAL
        image_extensions: Supported image extensions. Default is None which
                          will use only the supported extensions that
                          can be OPENd and SAVEd by PIL on your machine.
    """
    if types is None:
        types = {'.docx', '.pptx', '.xslx'}
    else:
        if isinstance(types, str):
            types = {types}
        else:
            types = {i for i in types}
    if output is None:
        output = os.getcwd()
    else:
        if os.path.splitext(output)[1]:
            # A file but it may not exist so you can't .isfile it
            output = os.path.dirname(output)
        else:
            output = output
        os.makedirs(output, exist_ok=True)

    if verbosity is not Verbosity.NONE:
        printer_callback = partial(printer, verbosity=verbosity)
        output_record = {
            'compressed_files': [],
            'errors': [],
            'image_errors': [],
            'images_total': 0,
            'images_compressed': 0,
            'images_skipped': 0,
            'images_converted': 0,
            'total_bytes': 0,
            'total_bytes_compressed': 0,
        }
        totaler_callback = partial(totaler, output_record)
    if image_extensions is None:
        registered_extensions = Image.registered_extensions()
        image_extensions = {
            ext for ext, func in registered_extensions.items()
            if func in Image.SAVE
            if func in Image.OPEN
        }
    stopped = False
    with ProcessPoolExecutor() as executor:
        if stopped:
            print('Shutting down executor...')
            executor.shutdown(cancel_futures=True)
            return
        for root, dirs, files in os.walk(cwd):
            for f in files:
                if stopped:
                    print('Shutting down executor...')
                    executor.shutdown(cancel_futures=True)
                    return
                if os.path.splitext(f)[1].lower() in types:
                    fpath = os.path.join(root, f)
                    outpath = os.path.join(output, f)
                    if overwrite or not os.path.isfile(outpath):
                        future = executor.submit(
                            process,
                            fpath,
                            output=outpath,
                            convert=convert,
                            image_extensions=image_extensions,
                        )
                        if verbosity is not Verbosity.NONE:
                            future.add_done_callback(totaler_callback)
                            future.add_done_callback(printer_callback)
    if verbosity is not Verbosity.NONE:
        print_total(output_record, verbosity)


def listdir(
    cwd,
    *,
    types=None,
    overwrite=False,
    output=None,
    convert=False,
    verbosity=Verbosity.NORMAL,
    image_extensions=None,
):
    """
    Iterates over the files in the directory and attempts to compress
    them if they match the listed file types

    Args:
        cwd: Path to directory to use

    Kwargs:
        types: Office filetype extension(s) to use.
               Accepts either a str or list-like object.
               Default is None which will use .docx, .pptx, and .xlsx
        overwrite: Overwrite if output exists. Default is False
        convert: Convert TIFFs to JPEGs. Default is False
        verbosity: Verbosity level. Default is Verbosity.NORMAL
        image_extensions: Supported image extensions. Deafult is None which
                          will use only the supported extensions that
                          can be OPENd and SAVEd by PIL on your machine.
    """
    if types is None:
        types = {'.docx', '.pptx', '.xslx'}
    else:
        if isinstance(types, str):
            types = {types}
        else:
            types = {i for i in types}
    if output is None:
        output = os.getcwd()
    else:
        if os.path.splitext(output)[1]:
            # A file but it may not exist so you can't .isfile it
            output = os.path.dirname(output)
        else:
            output = output
        os.makedirs(output, exist_ok=True)

    if verbosity is not Verbosity.NONE:
        printer_callback = partial(printer, verbosity=verbosity)
        output_record = {
            'compressed_files': [],
            'errors': [],
            'image_errors': [],
            'images_total': 0,
            'images_compressed': 0,
            'images_skipped': 0,
            'images_converted': 0,
            'total_bytes': 0,
            'total_bytes_compressed': 0,
        }
        totaler_callback = partial(totaler, output_record)
    if image_extensions is None:
        registered_extensions = Image.registered_extensions()
        image_extensions = {
            ext for ext, func in registered_extensions.items()
            if func in Image.SAVE
            if func in Image.OPEN
        }
    stopped = False
    with ProcessPoolExecutor() as executor:
        if stopped:
            print('Shutting down executor...')
            executor.shutdown(cancel_futures=True)
            return
        for item in os.listdir(cwd):
            if stopped:
                print('Shutting down executor...')
                executor.shutdown(cancel_futures=True)
                return
            fpath = os.path.join(cwd, item)
            if os.path.isfile(fpath):
                if os.path.splitext(fpath)[1].lower() in types:
                    outpath = os.path.join(output, item)
                    if overwrite or not os.path.isfile(outpath):
                        future = executor.submit(
                            process,
                            fpath,
                            output=outpath,
                            convert=convert,
                            image_extensions=image_extensions,
                        )
                        if verbosity is not Verbosity.NONE:
                            future.add_done_callback(totaler_callback)
                            future.add_done_callback(printer_callback)
    if verbosity is not Verbosity.NONE:
        print_total(output_record, verbosity)


def process(
    fpath,
    *,
    output,
    convert=False,
    image_extensions=None,
):
    """
    Attempts to compress the images found in the Office File

    Args:
        fpath: File path for the Office File

    Kwargs:
        output: File path for the compressed output.
        convert: Convert TIFFs to JPEGs. Default is False
        image_extensions: Supported image extensions. Deafult is None which
                          will use only the supported extensions that
                          can be OPENd and SAVEd by PIL on your machine.

    Returns:
        CompressionRecord: namedtuple of the results
    """
    if image_extensions is None:
        registered_extensions = Image.registered_extensions()
        image_extensions = {
            ext for ext, func in registered_extensions.items()
            if func in Image.SAVE
            if func in Image.OPEN
        }
    num_images_compressed = 0
    num_images_converted = 0
    num_images_skipped = 0
    start_size = os.stat(fpath).st_size
    errors = []
    conversions = []

    with zipfile.ZipFile(fpath, 'r') as in_zip:
        with tempfile.NamedTemporaryFile(mode='rb+') as tmp_file:
            with zipfile.ZipFile(tmp_file, 'w') as out_zip:
                out_zip.comment = in_zip.comment
                for item in in_zip.infolist():
                    fname, ext = os.path.splitext(item.filename)
                    ext = ext.lower()
                    if convert and (ext == '.xml' or ext == '.rels'):
                        continue
                    if convert and ext == '.tiff':
                        out_arcname = f'{fname}.jpeg'
                        try:
                            conversions.append(
                                (
                                    os.path.split(item.filename)[1].encode(),
                                    os.path.split(out_arcname)[1].encode()
                                )
                            )
                        except UnicodeError:
                            errors.append(
                                f'ERROR: Could not encode {item.filename} '
                                f'and/or {out_arcname}. '
                                'Conversion and compression will be skipped.'
                            )
                            num_images_skipped += 1
                            out_zip.writestr(item, in_zip.read(item.filename))
                        else:
                            try:
                                converted_image = convert_image(
                                    in_zip.read(item.filename)
                                )
                            except Exception as e:
                                errors.append(
                                    'ERROR: Could not convert '
                                    f'{item.filename}. Conversion and '
                                    f'compression will be skipped.\n{str(e)}'
                                )
                                num_images_skipped += 1
                                out_zip.writestr(
                                    item, in_zip.read(item.filename)
                                )
                            else:
                                num_images_converted += 1
                                converted_image.seek(0)
                                out_zip.writestr(
                                    out_arcname, converted_image.read()
                                )
                    elif ext in image_extensions:
                        try:
                            compressed_image = compress_image(
                                in_zip.read(item.filename)
                            )
                        except Exception as e:
                            errors.append(
                                f'ERROR: Could not compress {item.filename}: '
                                f'{str(e)}'
                            )
                            num_images_skipped += 1
                            out_zip.writestr(item, in_zip.read(item.filename))
                        else:
                            if item.file_size > compressed_image.tell() > 0:
                                num_images_compressed += 1
                                compressed_image.seek(0)
                                out_zip.writestr(item, compressed_image.read())
                            else:
                                num_images_skipped += 1
                                out_zip.writestr(
                                    item, in_zip.read(item.filename)
                                )
                    else:
                        out_zip.writestr(item, in_zip.read(item.filename))
                if convert:
                    for item in in_zip.infolist():
                        ext = os.path.splitext(item.filename)[1].lower()
                        if ext == '.xml' or ext == '.rels':
                            out_xml = in_zip.read(item.filename)
                            for orig_image, converted_image in conversions:
                                out_xml = out_xml.replace(
                                    orig_image, converted_image
                                )
                            out_zip.writestr(item, out_xml)
            with open(output, 'wb') as f:
                tmp_file.seek(0)
                f.write(tmp_file.read())
    return CompressionRecord(
        filename=fpath,
        errors=errors,
        num_images_compressed=num_images_compressed,
        num_images_converted=num_images_converted,
        num_images_skipped=num_images_skipped,
        start_size=start_size,
        compressed_size=os.stat(output).st_size,
    )


def compress_image(image_bytes, quality=75):
    """
    Compresses image if it is of a format of JPEG, PNG, or TIFF.

    Args:
        image: image to compress as bytes. Image must support `.read()`

    Kwargs:
        quality: Defaults to 75, which is PIL's default quality value
                 Only applicable to JPEG and TIFFs

    Returns:
        io.BytesIO object positioned at laste write
    """
    bytes_io_image = io.BytesIO()
    pil_image = Image.open(io.BytesIO(image_bytes))
    if pil_image.format == 'JPEG':
        pil_image.save(
            bytes_io_image, format='JPEG', quality=quality, optimize=True
        )
    elif pil_image.format == 'PNG':
        pil_image.save(bytes_io_image, format='PNG', optimize=True)
    elif pil_image.format == 'TIFF':
        pil_image.save(bytes_io_image, format='TIFF', quality=quality)
    return bytes_io_image


def convert_image(image_bytes, quality=75):
    """
    Converts image to JPG

    Args:
        image: image to convert as bytes. Image must support `.read()`

    Kwargs:
        quality: Defaults to 75, which is PIL's default quality value

    Returns:
        io.BytesIO object positioned at laste write
    """
    bytes_io_image = io.BytesIO()
    pil_image = Image.open(io.BytesIO(image_bytes))
    pil_image = pil_image.convert('RGB')
    pil_image.save(
        bytes_io_image, 'JPEG', quality=quality, optimize=True
    )
    return bytes_io_image


def printer(future, verbosity=Verbosity.NORMAL):
    try:
        result = future.result()
    except Exception as e:
        print(e)
    else:
        if verbosity is Verbosity.LOW:
            if result.num_images_compressed:
                print(
                    f'Compressed {result.filename}. '
                    f'{len(result.errors):,} Error(s) encountered.'
                )
        elif verbosity is Verbosity.NORMAL:
            if result.num_images_compressed:
                print(
                    f'Filename: {result.filename}.'
                    '\n'
                    f'Results: '
                    f'{result.num_images_compressed:,} compressed, '
                    f'{result.num_images_converted:,} converted, '
                    f'{result.num_images_skipped:,} skipped'
                    '\n'
                    f'Errors: {len(result.errors):,}'
                )
            else:
                print(
                    f'No compressed images for {result.filename}. '
                    f'{len(result.errors):,} Error(s) encountered.'
                )
        elif verbosity is Verbosity.HIGH:
            errors = "\n\t".join(result.errors) if result.errors else 'None!'
            print(
                ''.join(
                    [
                        f'Filename: {result.filename}.',
                        '\n',
                        'Results: ',
                        f'\n\t{result.num_images_compressed:,} compressed',
                        f'\n\t{result.num_images_converted:,} converted',
                        f'\n\t{result.num_images_skipped:,} skipped',
                        '\n',
                        f'Errors: {errors}'
                    ]
                )
            )


def totaler(output_record, future):
    try:
        result = future.result()
    except Exception as e:
        output_record['errors'].append(str(e))
    else:
        total_images = sum(
            [
                result.num_images_compressed,
                result.num_images_converted,
                result.num_images_skipped,
            ]
        )
        if total_images:
            output_record['compressed_files'].append(result.filename)
            output_record['images_total'] += total_images
            output_record['images_compressed'] += result.num_images_compressed
            output_record['images_skipped'] += result.num_images_skipped
            output_record['images_converted'] += result.num_images_converted
            output_record['total_bytes'] += result.start_size
            output_record['total_bytes_compressed'] += result.compressed_size
            output_record['image_errors'].extend(result.errors)


def print_total(record, verbosity):
    if verbosity is Verbosity.LOW:
        print(
            f'Compressed {len(record["compressed_files"]):,} '
            f'document(s) with {len(record["image_errors"]):,} '
            'image(s) that could not be converted and '
            f'{len(record["errors"]):,} document(s) '
            'that failed.'
        )
    elif verbosity is Verbosity.NORMAL:
        if record['total_bytes_compressed'] > 0:
            gb = 1024 * 1024 * 1024
            mb = 1024 * 1024
            kb = 1024
            total_cmp = record['total_bytes_compressed']
            if total_cmp > gb:
                savings = f'{total_cmp / gb:.2f} GB'
            elif total_cmp > mb:
                savings = f'{total_cmp / mb:.2f} MB'
            elif total_cmp > kb:
                savings = f'{total_cmp / kb:.2f} KB'
            else:
                if total_cmp < 1:
                    total_cmp = '<1'
                savings = f'{total_cmp} bytes'
            output = f'Compressed {len(record["compressed_files"]):,} '
            output += 'document(s)\n'
            output += f'\n{record["images_compressed"]:,} '
            output += 'image(s) were '
            output += f'compressed for a savings of {savings}'
            output += '\n'
            if record['images_converted'] > 0:
                output += f'{record["images_converted"]:,} '
                output += 'image(s) were converted from TIFF to JPG\n'
            if record['image_errors']:
                output += f'{len(record["image_errors"]):,} '
                output += 'image(s) could not be converted or compressed\n'
            if record['errors']:
                output += f'{len(record["errors"]):,} document(s) '
                output += 'could not be compressed due to error'
        else:
            output = 'No images were compressed'
        print(output)
    elif verbosity is Verbosity.HIGH:
        if record['total_bytes_compressed'] > 0:
            gb = 1024 * 1024 * 1024
            mb = 1024 * 1024
            kb = 1024
            total_cmp = record['total_bytes_compressed']
            if total_cmp > gb:
                savings = f'{total_cmp / gb:.2f} GB'
            elif total_cmp > mb:
                savings = f'{total_cmp / mb:.2f} MB'
            elif total_cmp > kb:
                savings = f'{total_cmp / kb:.2f} KB'
            else:
                if total_cmp < 1:
                    total_cmp = '<1'
                savings = f'{total_cmp} bytes'
            output = f'Compressed {len(record["compressed_files"]):,} '
            output += 'document(s):\n\t'
            output += '\n\t'.join(record['compressed_files'])
            output += f'\n{record["images_compressed"]:,} '
            output += 'image(s) were '
            output += f'compressed for a savings of {savings}'
            output += '\n'
            if record['images_converted'] > 0:
                output += f'{record["images_converted"]:,} '
                output += 'image(s) were converted from TIFF to JPG\n'
            if record['image_errors']:
                output += f'{len(record["image_errors"]):,} '
                output += 'image(s) could not be converted or compressed\n'
            if record['errors']:
                output += 'ERRORS:\n\t'
                output += '\n\t'.join(record["errors"])
            else:
                output += 'No errors received!'
        else:
            output = 'No images were compressed'
        print(output)
