import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { useLocation } from "react-router";
import { useHistory } from "react-router-dom";
import { Select } from "antd";
import { SearchOutlined, CaretDownFilled, CaretUpFilled, MinusOutlined } from "@ant-design/icons";
import styled from "styled-components";
import axios from "axios";
import Loading from "./Loading";

const StockStyled = styled.div`
  width: 80%;
  margin: 0 auto;

  .apexcharts-toolbar {
    display: none;
  }

  .market-chart {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
    height: 100%;

    .chart-item {
      margin: 20px;
      padding: 20px;
      background-color: #fbfbfb;
      border-radius: 5px;

      .chart-text {
        margin-bottom: 15px;
        font-size: 1rem;
        font-weight: 700;
        text-align: center;
      }

      .chart-graph {
        min-width: 450px;
      }
    }
  }

  .stock-detail {
    display: flex;
    justify-content: space-between;
    padding: 20px 30px;
    background-color: #fbfbfb;
    border-radius: 5px;

    .detail-info {
      display: flex;
      justify-content: center;
      flex-direction: column;
      width: 25%;
      min-width: 150px;
      margin-right: 50px;

      .stock-item {
        text-align: center;
        .stock-name {
          font-size: 20px;
          font-weight: 700;
        }

        .stock-code {
          font-size: 14px;
        }

        .stock-price {
          font-size: 28px;
          font-weight: 700;
          margin: 10px 0 20px;
          padding: 10px;
          background-color: #3f47530d;
          border-radius: 5px;
        }

        .compare {
          font-weight: 500;
          font-size: 18px;

          .compare-extra {
            display: flex;
            justify-content: center;
            align-items: center;
            padding-bottom: 5px;

            .compare-text {
              position: relative;
              top: 1px;
              font-size: 13px;
            }

            div {
              margin: 0 8px;
            }
          }
        }

        .red {
          color: #ff0000;
        }

        .blue {
          color: #004eff;
        }

        table {
          width: 100%;
          font-weight: 700;
          text-align: left;
          justify-content: space-between;

          td {
            padding: 2px 5px;
            color: #3f4753;

            &.value {
              text-align: right;
            }
          }
        }
      }
    }

    .detail-chart {
      width: 75%;
      display: flex;
      flex-direction: column;

      .period-btns {
        text-align: right;
        padding-right: 10px;

        button {
          margin-left: 5px;
          padding: 2px 10px;
          font-size: 13px;
          font-weight: 700;
          background-color: #3f47530d;
          border: none;
          border-radius: 3px;
          cursor: pointer;
        }
      }
    }
  }
`;

const SelectStyled = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  width: 50%;
  margin: 30px auto;

  .ant-select {
    width: 100%;

    &.ant-select-focused {
      .ant-select-selector {
        border-color: #3f4753 !important;
        box-shadow: none !important;
      }
    }

    &:hover {
      border-color: #3f4753;

      .ant-select-selector {
        border-color: inherit;
        box-shadow: none;
      }
    }

    .ant-select-selector {
      height: 45px;
      line-height: 43px;
      padding-right: 45px;

      input {
        height: 100%;
        padding-right: 35px;
      }

      .ant-select-selection-item,
      .ant-select-selection-placeholder {
        line-height: inherit;
      }
    }
  }

  .search-icon {
    position: absolute;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 45px;
    height: 45px;
    color: #3f4753;
    font-size: 18px;
  }
`;

function Stock() {
  const history = useHistory();
  const { pathname } = useLocation();
  const [loading, setLoading] = useState(false);
  // 시장지수(국내, 해외)
  const [marketData, setMarketData] = useState({});
  // 검색한 종목과 일치하는 데이터(종목명, 코드)
  const [searchData, setSearchData] = useState([]);
  // 검색한 종목명
  const [searchText, setSearchText] = useState("");
  // 검색한 종목의 상세정보, 기간 차트정보
  const [detailData, setDetailData] = useState({});
  // 차트 기간 선택값
  const [period, setPeriod] = useState("week");

  const { Option } = Select;

  useEffect(() => {
    const splitPath = pathname.split("/");
    if (splitPath && splitPath[2]) {
      const code = splitPath[2];
      // 종목 상세 정보 조회
      onGetStockDetail(code);
    } else {
      // 시장지수 조회
      onGetStockMarket();
    }
  }, [pathname]);

  // 시장 지수 조회
  const onGetStockMarket = async () => {
    setLoading(true);
    await axios
      .get("/api/chart/stock")
      .then((res) => {
        const chartData = [];
        if (Object.keys(res.data).length > 0) {
          Object.keys(res.data).forEach((key) => {
            const chartY = [];
            const chartX = [];
            res.data[key].forEach((data) => {
              chartY.push(data.index.toFixed(2));
              chartX.push(data.date);
            });

            let marketText = "";
            if (key === "KOSPI") {
              marketText = "코스피(KOSPI)";
            } else if (key === "KOSDAQ") {
              marketText = "코스닥(KOSDAQ)";
            } else if (key === "DOW") {
              marketText = "다우(DOW)";
            } else if (key === "NASDAQ") {
              marketText = "나스닥(NASDAQ)";
            } else if (key === "SP500") {
              marketText = "S&P 500";
            } else if (key === "SH") {
              marketText = "상해(SH)";
            }

            chartData.push({
              text: marketText,
              series: {
                name: key,
                data: chartY,
              },
              options: {
                chart: {
                  id: key,
                },
                xaxis: {
                  categories: chartX,
                },
              },
            });
          });
        }
        setMarketData(chartData);
        setLoading(false);
      })
      .catch((error) => {
        console.log("onGetStockMarket", error);
      });
  };

  // 종목명 입력 이벤트
  const onChangeSearch = (value) => {
    setSearchText(value);

    if (value) {
      onGetMatchedStock(value);
    }
  };

  // 검색 문자열과 일치하는 주식 리스트 조회
  const onGetMatchedStock = async (value) => {
    if (!value) return;

    await axios
      .get(`/api/searchstock/${value}`)
      .then((res) => {
        setSearchData(res.data);
      })
      .catch((error) => {
        console.log("onGetMatchedStock", error);
      });
  };

  // 검색한 종목 선택 이벤트
  const onShowDetail = (value) => {
    history.push(`/stock/${value}`);
  };

  // 종목 드롭다운 리스트
  const stockDropdown = searchData?.map((data) => <Option key={data.code}>{data.name}</Option>);

  // 종목 상세 정보 조회
  const onGetStockDetail = async (code) => {
    if (!code) return;
    setLoading(true);

    await axios
      .get(`/api/getstock/${code}`)
      .then((res) => {
        const detailChartData = {};
        if (Object.keys(res.data).length > 0) {
          Object.keys(res.data).forEach((key) => {
            if (key === "info") return;

            const chartY = [];
            const chartX = [];
            res.data[key].forEach((data) => {
              chartY.push(data.index.toFixed(2));
              chartX.push(data.date);
            });

            detailChartData[key] = {
              series: {
                name: key,
                data: chartY,
              },
              options: {
                chart: {
                  id: key,
                },
                xaxis: {
                  categories: chartX,
                },
              },
            };
          });
        }

        setDetailData({
          info: res.data.info[0],
          week: detailChartData["week"],
          month: detailChartData["month"],
          year: detailChartData["year"],
        });

        setLoading(false);
      })
      .catch((error) => {
        console.log("onGetStockDetail", error);
      });
  };

  // 전일대비 비교 값
  let compare = { status: "same", icon: null, value: 0, rate: "0.00%" };
  if (detailData?.info) {
    const { closing, price } = detailData.info;
    // 등락율
    const rate = (((price - closing) / closing) * 100).toFixed(2);

    if (closing > price) {
      compare = { status: "down", icon: <CaretDownFilled />, value: closing - price, rate: `${rate}%` };
    } else if (closing < price) {
      compare = { status: "up", icon: <CaretUpFilled />, value: price - closing, rate: `${rate}%` };
    }
  }

  // 천 단위로 콤마(,) 표시
  const addComma = (number) => {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  // 차트 기간 변경 시
  const changePeriod = (term) => {
    setPeriod(term);
  };

  return (
    <StockStyled>
      <Loading loading={loading} />

      <SelectStyled>
        <Select
          showSearch
          value={searchText || null}
          placeholder="종목명 검색"
          defaultActiveFirstOption={false}
          showArrow={false}
          filterOption={false}
          onSearch={onChangeSearch}
          onChange={onShowDetail}
          notFoundContent="검색 결과가 없습니다."
        >
          {stockDropdown}
        </Select>
        <div className="search-icon">
          <SearchOutlined />
        </div>
      </SelectStyled>

      {detailData?.info ? (
        <>
          <div className="stock-detail">
            <div className="detail-info">
              <div className="stock-item">
                <span className="stock-name">{detailData.info.name}</span>
                <span className="stock-code">{` (${detailData.info.code})`}</span>
              </div>
              <div className="stock-item">
                <div
                  className={`stock-price ${compare.status === "up" ? "red" : ""}${
                    compare.status === "down" ? "blue" : ""
                  }`}
                >
                  <div>{addComma(detailData.info.price)}</div>
                  <div className="compare">
                    <div className="compare-extra">
                      <div className="compare-text">{`전일대비 `} </div>
                      <div>
                        {compare.icon}
                        {addComma(compare.value)}
                      </div>
                      <div>{compare.rate}</div>
                    </div>
                  </div>
                </div>

                <table>
                  <tbody>
                    <tr>
                      <td>전일</td>
                      <td className="value">{addComma(detailData.info.closing)}</td>
                    </tr>
                    <tr>
                      <td>시가</td>
                      <td className="value">{addComma(detailData.info.opening)}</td>
                    </tr>
                    <tr>
                      <td>고가</td>
                      <td className="value">{addComma(detailData.info.high)}</td>
                    </tr>
                    <tr>
                      <td>저가</td>
                      <td className="value">{addComma(detailData.info.low)}</td>
                    </tr>
                    <tr>
                      <td>거래량</td>
                      <td className="value">{addComma(detailData.info.trading_volume)}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div className="detail-chart">
              <div className="period-btns">
                <button onClick={() => changePeriod("week")}>일주일</button>
                <button onClick={() => changePeriod("month")}>한 달</button>
                <button onClick={() => changePeriod("year")}>일 년</button>
              </div>
              {detailData && detailData[period] && (
                <Chart
                  className="detail-chart-graph"
                  options={detailData[period].options}
                  series={[detailData[period].series]}
                  type="line"
                  height={300}
                />
              )}
            </div>
          </div>
        </>
      ) : (
        <>
          <div className="market-chart">
            {marketData?.length > 0 &&
              marketData?.map((data) => {
                return (
                  <div className="chart-item" key={data.text}>
                    <div className="chart-text">{data.text}</div>
                    <Chart className="chart-graph" options={data.options} series={[data.series]} type="line" />
                  </div>
                );
              })}
          </div>
        </>
      )}
    </StockStyled>
  );
}

export default Stock;
