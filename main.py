import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기
url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
df = pd.read_csv(url)

# 여러 장르가 있으면 첫 번째 장르만 사용
df["genre_first"] = (
    df["genre"]
    .fillna("장르 미상")
    .astype(str)
    .str.split("|")
    .str[0]
)

# 숫자형으로 변환
df["total_audi"] = pd.to_numeric(df["total_audi"], errors="coerce")


# =============================
# 1. 장르별 영화 편수
# =============================
st.header("1. 장르별 영화 편수")

genre_count = df["genre_first"].value_counts().reset_index()
genre_count.columns = ["장르", "영화 편수"]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="percent",
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "어떤 장르의 영화가 가장 많이 포함되어 있는지 알 수 있다."
)

st.divider()


# =============================
# 2. 장르별 영화 총 관객 트리맵
# =============================
st.header("2. 장르별 영화 총 관객")

treemap_df = df.dropna(subset=["total_audi"]).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "각 장르에 어떤 영화가 포함되어 있고, 영화별 총 관객 규모가 얼마나 다른지 알 수 있다."
)

st.divider()


# =============================
# 3. 총 관객수 히스토그램
# =============================
st.header("3. 총 관객수 분포")

hist_df = df.dropna(subset=["total_audi"]).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객수 분포",
    labels={"total_audi": "총 관객수", "count": "영화 편수"}
)

fig3.update_traces(
    hovertemplate=(
        "총 관객수 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

st.plotly_chart(fig3, use_container_width=True)

# 대부분의 영화가 몰려 있는 구간 계산
counts, bins = pd.cut(
    hist_df["total_audi"],
    bins=20,
    include_lowest=True,
    retbins=True
), None

bin_counts = hist_df["total_audi"].groupby(
    pd.cut(hist_df["total_audi"], bins=20, include_lowest=True)
).size()

most_common_bin = bin_counts.idxmax()

# 가장 관객이 많은 영화
max_row = hist_df.loc[hist_df["total_audi"].idxmax()]
max_movie = max_row["movieNm"]
max_audience = int(max_row["total_audi"])

st.markdown(
    f"**이 그래프로 알 수 있는 것:** "
    f"대부분의 영화는 **{most_common_bin.left:,.0f}명 ~ {most_common_bin.right:,.0f}명** "
    f"구간에 몰려 있다. "
    f"가장 관객이 많은 영화는 **{max_movie}**로, "
    f"총 **{max_audience:,}명**의 관객을 기록했다."
)

st.divider()
