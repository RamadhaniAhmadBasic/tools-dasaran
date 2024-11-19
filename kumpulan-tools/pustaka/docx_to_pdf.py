from docx2pdf import convert
import pustaka.tabel_info

def f():
	docx_file_path = input("Masukkan direktori tempat file DOCX berada: ")
	pdf_file_path = input("Masukkan nama file PDF output: ")
	convert(docx_file_path, pdf_file_path)
	pustaka.tabel_info.f("SUCCESS", f"Konversi {docx_file_path} ke {pdf_file_path}")
