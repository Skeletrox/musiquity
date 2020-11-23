import React, { Component } from 'react'
import Chart from "chart.js";
import { getUserMetrics } from "../actions/actions.js";


export default class MyChart extends Component {
    chartRef = React.createRef();


    constructor(props) {
        super(props);
        this.state = {
            dummy: this.props.hr
        };   
    }

    componentDidMount() {
        const myChartRef = this.chartRef.current.getContext("2d");

        getUserMetrics(this.props.user, (res, err) => {
            if (err) {
                console.log(err);
                return;
            }
            let lables = res.map((item, index) => {
                return item.x
            });
            new Chart(myChartRef, {
                type: "line",
                data: {
                    labels: lables,
                    datasets: [
                        {
                            label: "Heart Rate",
                            data: res
                        }
                    ]
                }
            })
        });
    }

    render() {
        return (
            <div>
                <canvas id="myChart" ref={this.chartRef} />
            </div>
        )
    }
}