import streamlit as st 
import pandas as pd
from load_data import get_data
import plotly.graph_objects as go
from datetime import datetime
import plotly.express as px

st.logo("logo.png",size= 'large')
unit = '2U82'
##Mặc định không mở sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        margin-top: 200 px;
        color: 'rgb(255,255,255)';
        font-size : 48px;
    }
    div.block-container{padding-top:0rem};
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(f'<h1 class="centered-title">OEE MÁY CẮT {unit}</h1>', unsafe_allow_html=True)

df_today = get_data(DB='AUTO_CUT_RG',
    query=f"Select MCName,WorkDate,OEE,TotalTime,TotalTable from OEE_New where MCName = 'MAYCAT{unit}' AND WORKDATE >= CONVERT(DATE,DATEADD(DAY,0,GETDATE())) Order by WorkDate")
df_15 = get_data(DB='AUTO_CUT_RG',query=f"Select MCName,WorkDate,OEE,TotalTime,TotalTable from OEE_New where MCName = 'MAYCAT{unit}' AND WORKDATE >= DATEADD(DAY,-15,GETDATE()) Order by WorkDate")
df_tg = get_data(DB='AUTO_CUT_RG',query=f"Select * from Target_OEE where MachineName = '{unit}'")

df_today['%OEE'] = df_today['OEE']/df_today['TotalTime']
df_today['MCName'] = df_today['MCName'].str.replace("MAYCAT", "", regex=False)
df_today = pd.merge(df_today,df_tg,left_on='MCName',right_on='MachineName')
df_today.rename(columns={"Targer": "OEE target"}, inplace=True)

df_stop_today = get_data(DB='AUTO_CUT_RG',query=f"Select * from STOP_TIME where MachineName = '{unit}' and Ngay = convert(date,getdate()) order by TuGio_Gio,TuGio_Phut") #
df_stop_15 = get_data(DB='AUTO_CUT_RG',query=f"Select * from STOP_TIME where MachineName = '{unit}' and Ngay >= dateadd(day,-15,getdate())")

current_date = datetime.now().strftime("%d/%m")
current_date_time = datetime.now().strftime("%d/%m %H:%M")

cols = st.columns([1,2.5])

with cols[0]:
    oee_today = df_today['%OEE'].mean()
    oee_target = df_today['OEE target'].mean()

    # Xác định màu thanh và màu delta
    if oee_today < oee_target - 0.1:
        color = "red"
        delta_color = "red"
    elif oee_today < oee_target :
        color = "yellow"
        delta_color = "yellow"
    elif oee_today < oee_target + 0.1:
        color = "green"
        delta_color = "green"
    else:
        color = "purple"
        delta_color = "purple"

    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = oee_today * 100,
        number = {
            "suffix": "%",
            "valueformat": ".1f"
        },
        delta = {
        "reference": oee_target * 100,
        "increasing": {"color": delta_color},
        "decreasing": {"color": delta_color},
        "valueformat": ".1f",  # 1 số thập phân
        "suffix": "%"
        },
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.75,
                'value': oee_target * 100
            },
            'steps': [
                {'range': [0, oee_target * 90], 'color': '#ffcccc'},         # đỏ nhạt
                {'range': [oee_target * 90, oee_target * 100], 'color': '#fff3cd'},  # vàng nhạt
                {'range': [oee_target * 100, oee_target * 110], 'color': '#d4edda'}, # xanh nhạt
                {'range': [oee_target * 110, 100], 'color': '#e5ccff'}       # tím nhạt
            ],
        },
    ))
    fig.update_layout(
    # margin=dict(t=110, b=10, l=30, r=30),  # giảm top, bottom
    height=400,
    title={
        'text': f"<b>OEE {current_date_time}</b>",
        'font': {'size': 40},
        'x': 0.5,  # căn giữa (nếu muốn)
        'xanchor': 'center'
    }
    )

    st.plotly_chart(fig, use_container_width=True)
    ### stop time
    df_stop_today['Từ'] = df_stop_today['TuGio_Gio'].astype(str).str.zfill(2) + ':' + df_stop_today['TuGio_Phut'].astype(str).str.zfill(2)
    df_stop_today['Đến'] = df_stop_today['DenGio_Gio'].astype(str).str.zfill(2) + ':' + df_stop_today['DenGio_Phut'].astype(str).str.zfill(2)
    df_stop_today.rename(columns={'SoPhut':'Số phút dừng','LyDo' : 'Lý do dừng','GhiChu' : 'Ghi chú'},inplace=True)
    df_stop_today = df_stop_today[['Từ','Đến','Số phút dừng','Lý do dừng','Ghi chú']]
    st.subheader(f"Lý do dừng máy {current_date}")
    # Chèn CSS để chỉnh header bảng st.table
    st.markdown("""
        <style>
        table thead th {
            background-color: #2b2b2b !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 20px !important;
            text-align: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hiển thị bảng
    st.table(df_stop_today)
with cols[1]:
    df_15['%OEE'] = df_15['OEE']/df_15['TotalTime']
    df_15['MCName'] = df_15['MCName'].str.replace("MAYCAT","",regex=True)
    df_15 = pd.merge(df_15,df_tg,left_on='MCName',right_on='MachineName')
    df_15.rename(columns={"Targer": "OEE target"}, inplace=True)
    # df_15
    df = df_15.copy()

    # Chuyển WorkDate thành datetime và format
    df['WorkDate'] = pd.to_datetime(df['WorkDate'])
    df = df.sort_values('WorkDate')
    df['WorkDate_str'] = df['WorkDate'].dt.strftime('%d/%m')

    # Tô màu OEE theo target
    def get_oee_color(row):
        if row['%OEE'] < row['OEE target'] - 0.1:
            return 'red'
        elif row['%OEE'] < row['OEE target']:
            return 'yellow'
        elif row['%OEE'] < row['OEE target'] + 0.1:
            return 'green'
        else:
            return 'purple'

    df['OEE_color'] = df.apply(get_oee_color, axis=1)

    # Vẽ biểu đồ
    fig = go.Figure()

    # CỘT: TotalTable + label ở phía dưới
    fig.add_trace(go.Bar(
        x=df['WorkDate_str'],
        y=df['TotalTable'],
        name='Total Table',
        marker_color='lightblue',
        text=df['TotalTable'],
        textposition='inside', 
        insidetextanchor='start',
        textfont=dict(color='black',size = 20),
        yaxis='y1'
    ))

    # LINE: %OEE + label ở phía trên, màu theo logic
    fig.add_trace(go.Scatter(
        x=df['WorkDate_str'],
        y=df['%OEE'] * 100,
        mode='markers+lines+text',
        name='% OEE',
        marker=dict(color=df['OEE_color'], size=20),
        line=dict(color='gray', width=2),
        text=[f"{val:.1f}%" for val in df['%OEE'] * 100],
        textposition='top center',
        textfont=dict(color='white',size = 20),
        hovertemplate='OEE: %{text}<extra></extra>',
        yaxis='y2'
    ))

    # Layout
    y_max = df['TotalTable'].max()*2
    fig.update_layout(
        title = {
        'text': "Biểu đồ tổng số bàn cắt và %OEE 15 ngày gần nhất",
        'font': {'size': 32},  
        },
        xaxis=dict(title="",tickfont = dict(size = 15)),
        yaxis=dict(title="Tổng số bàn cắt", side="left",range=[0, y_max]),
        yaxis2=dict(
            title="% OEE",
            overlaying="y",
            side="right",
            tickformat=".0f",
            range=[0, 120]
        ),
        showlegend=False,
        height=400,
        template='plotly_white',
    )

    st.plotly_chart(fig, use_container_width=True)
    #########
    # xử lý stop time
    st.subheader("Tổng số phút dừng máy 15 ngày gần nhất theo lý do")

    cols = st.columns(2)
    with cols[0]:
        df_stop_15_lydo= df_stop_15.groupby(by='LyDo').agg({'SoPhut':'sum','MachineName':'count'}).reset_index()
        df_stop_15_lydo.rename(columns={'MachineName':'Số lần dừng','LyDo':'Lý do dừng','SoPhut':'Số phút dừng'},inplace=True)
        fig = go.Figure()
        fig.add_trace(go.Pie(
        labels=df_stop_15_lydo['Lý do dừng'],
        values=df_stop_15_lydo['Số phút dừng'],
        hovertemplate="<b>%{label}</b><br>Số phút dừng: %{value}<br>Số lần dừng: %{customdata}",
        customdata=df_stop_15_lydo['Số lần dừng'],
        textinfo='label+percent',
        textfont_size=20,
        textposition='outside',
        marker=dict(line=dict(color='#000000', width=1))
        ))

        fig.update_layout(
            height=300,
            showlegend=False,
            margin=dict(t=20, b=20, l=10, r=10)
        )
        st.plotly_chart(fig,use_container_width=True)
    with cols[1]:
        df_stop_15_ghichu= df_stop_15.groupby(by=['LyDo','GhiChu']).agg({'SoPhut':'sum','MachineName':'count'}).reset_index()
        df_stop_15_ghichu.rename(columns={'MachineName':'Số lần dừng','LyDo':'Lý do dừng','SoPhut':'Số phút dừng','GhiChu':'Ghi chú'},inplace=True)

        st.table(df_stop_15_ghichu)
        

# Auto-refresh sau 15 phút (900,000 ms)
st.markdown("""
    <meta http-equiv="refresh" content="300">
""", unsafe_allow_html=True)
