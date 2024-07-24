import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize-matplotlib

# Load the CSV file
file_path = '202406_202406_연령별인구현황_월간 (1).csv'
data = pd.read_csv(file_path, encoding='cp949')

# Extract columns for elementary (6-11 years old) and middle school (12-14 years old) age groups
age_columns = {
    '6-11': ['2024년06월_계_6세', '2024년06월_계_7세', '2024년06월_계_8세', '2024년06월_계_9세', '2024년06월_계_10세', '2024년06월_계_11세'],
    '12-14': ['2024년06월_계_12세', '2024년06월_계_13세', '2024년06월_계_14세']
}

# Function to calculate population ratios
def calculate_ratios(region):
    region_data = data[data['행정구역'].str.contains(region)]
    if region_data.empty:
        st.error("해당 지역을 찾을 수 없습니다.")
        return None, None
    
    elementary_pop = region_data[age_columns['6-11']].replace(',', '', regex=True).astype(int).sum(axis=1).values[0]
    middle_pop = region_data[age_columns['12-14']].replace(',', '', regex=True).astype(int).sum(axis=1).values[0]
    
    return elementary_pop, middle_pop

# Streamlit app
st.title("지역별 초등학생 및 중학생 인구 비율")

region = st.text_input("지역을 입력하세요:", "서울특별시")

if region:
    elementary_pop, middle_pop = calculate_ratios(region)
    
    if elementary_pop is not None and middle_pop is not None:
        labels = ['초등학생 (6-11세)', '중학생 (12-14세)']
        sizes = [elementary_pop, middle_pop]
        colors = ['#ff9999','#66b3ff']

        fig1, ax1 = plt.subplots()
        ax1.pie
