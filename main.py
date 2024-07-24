import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate middle school student population
def calculate_middle_school_pop(region, data):
    region_data = data[data['행정구역'].str.contains(region)]
    if region_data.empty:
        st.error("해당 지역을 찾을 수 없습니다.")
        return None, None
    
    middle_school_columns = ['2023년12월_계_12세', '2023년12월_계_13세', '2023년12월_계_14세']
    middle_school_pop = region_data[middle_school_columns].replace(',', '', regex=True).astype(int).sum(axis=1).values[0]
    total_pop = region_data['2023년12월_계_총인구수'].replace(',', '', regex=True).astype(int).values[0]
    
    return middle_school_pop, total_pop

# Streamlit app
st.title("지역별 중학생 인구 비율")

try:
    # Load the CSV file
    file_path = '202312_202312_연령별인구현황_월간 (2).csv'
    data = pd.read_csv(file_path, encoding='cp949')
    
    region = st.text_input("지역을 입력하세요:", "서울특별시")

    if region:
        middle_school_pop, total_pop = calculate_middle_school_pop(region, data)
        
        if middle_school_pop is not None:
            labels = ['중학생 (12-14세)', '기타 인구']
            sizes = [middle_school_pop, total_pop - middle_school_pop]
            colors = ['#ff9999','#66b3ff']

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            st.pyplot(fig1)
except FileNotFoundError:
    st.error(f"파일을 찾을 수 없습니다: {file_path}")
except pd.errors.ParserError:
    st.error("CSV 파일을 파싱하는 동안 오류가 발생했습니다.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
