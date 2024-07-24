import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = '/mnt/data/202406_202406_연령별인구현황_월간 (1).csv'
data = pd.read_csv(file_path, encoding='cp949')

# Extract relevant columns
age_columns = ['2024년06월_계_6세', '2024년06월_계_7세', '2024년06월_계_8세', '2024년06월_계_9세', '2024년06월_계_10세', '2024년06월_계_11세']

# Function to calculate elementary student population
def calculate_elementary_pop(region):
    region_data = data[data['행정구역'].str.contains(region)]
    if region_data.empty:
        st.error("해당 지역을 찾을 수 없습니다.")
        return None
    
    elementary_pop = region_data[age_columns].replace(',', '', regex=True).astype(int).sum(axis=1).values[0]
    total_pop = region_data['2024년06월_계_총인구수'].replace(',', '', regex=True).astype(int).values[0]
    
    return elementary_pop, total_pop

# Streamlit app
st.title("지역별 초등학생 인구 비율")

region = st.text_input("지역을 입력하세요:", "서울특별시")

if region:
    elementary_pop, total_pop = calculate_elementary_pop(region)
    
    if elementary_pop is not None:
        labels = ['초등학생 (6-11세)', '기타 인구']
        sizes = [elementary_pop, total_pop - elementary_pop]
        colors = ['#ff9999','#66b3ff']

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)
