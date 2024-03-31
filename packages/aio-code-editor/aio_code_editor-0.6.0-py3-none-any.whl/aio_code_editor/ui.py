import streamlit as st
from code_editor import code_editor
from aio_code_editor.css import info_bar_input, info_bar_output, output_btns, input_btns
import subprocess
from aio_code_editor.until import check_code, write_code
import os

environ = os.environ.copy()
environ['PYTHONIOENCODING'] = 'utf-8'

def side_bar():
    with st.sidebar:
        st.markdown("## :heartbeat: :heartbeat: Hướng dẫn  :heartbeat: :heartbeat:")
        st.markdown("1. Đặt tên file (không bắt buộc)")
        st.markdown("2. Viết mã Python vào ô bên dưới")
        st.markdown("3. Nhấn nút **Run** để thực thi mã")
        st.markdown("4. Kết quả sẽ hiển thị ở ô bên dưới")
        st.markdown("5. Bạn có thể tải file Python bằng cách nhấn vào nút **Save file**")
        
        file_name = st.text_input("Tên file:", "st-test.py")
        st.write("Chill chút nhỉ? ^^")
        st.audio("https://cdn.pixabay.com/audio/2023/01/10/audio_5f83ba4572.mp3", format="audio/mp3")
        st.audio("https://cdn.pixabay.com/audio/2023/04/30/audio_6b3a512606.mp3", format="audio/mp3")
        st.audio("https://ia800209.us.archive.org/12/items/ECHOSAXEND/ECHOSAXEND.mp3", format="audio/mp3")
        
        return file_name
    
def heading():
    col_1, col_2, col_3 = st.columns([0.2, 0.5, 0.4])
    with col_2:
        st.title("AIO Code Editor")
    with col_3:
        st.image("https://ia800202.us.archive.org/30/items/shark_202403/shark.png", width=150)

def codes_box(sample_code, min_raw=5, max_raw=20):
    response_dict = code_editor(sample_code, buttons=input_btns, height=[min_raw, max_raw], info= info_bar_input)
    codes = response_dict["text"]
    type = response_dict["type"]
    return codes, type, response_dict

def output_box(response_dict, results, min_raw=5, max_raw=20):
    num_rows = response_dict['cursor']['row']
    if num_rows<=min_raw:
        num_rows = min_raw
    elif num_rows>=max_raw:
        num_rows = max_raw
    code_editor(results, buttons=output_btns, height= [num_rows, num_rows], info=info_bar_output)


def run_code(file_name, codes, type, response_dict, download=False):
    if check_code(codes):     
        if type == "submit":
            # Lưu mã vào file Python
            write_code(codes, file_name)
            # Hiển thị button đownload file
            if download:
                st.download_button(
                    label="Save file",
                    data=open(file_name, 'rb').read(),
                    file_name= file_name,
                    mime="text/plain")
            
            # Thực thi file Python và lấy đầu ra và lỗi (nếu có)
            result = subprocess.run(['python', file_name], encoding="utf-8", env=environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Hiển thị kết quả trong output_box
            output_box(response_dict, f"{result.stdout}\n{result.stderr}")
    else:
        st.error("Mã của bạn có thể nguy hiểm, vui lòng kiểm tra lại!")

def code_io(sample=''' ''', l=1, r=1, min_raw=5, max_raw=20, download=False):
    col1, col2 = st.columns([l, r])
    with col1:
        codes, type, response_dict = codes_box(sample, min_raw, max_raw)
    with col2:
        run_code(file_name="st-test.py", codes=codes, type=type, response_dict=response_dict, download=download)