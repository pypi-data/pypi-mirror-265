import streamlit.components.v1 as components
import json
import uuid


def my_chart_component(
    data,
    chart_type="bar",
    canvas_width=700,  # Set the canvas width for the chart
    canvas_height=700,  # Set the canvas height for the chart
    title="Custom Chart Title",
    legend_position="top",
    x_axis_title="Category",
    y_axis_title="Value",
):
    unique_id = uuid.uuid4().hex
    canvas_id = f"myChart-{unique_id}"

    data_json = json.dumps(data)
    options = {
        "plugins": {
            "legend": {
                "display": True,
                "position": legend_position,
            },
            "title": {
                "display": True,
                "text": title,
                "font": {
                    "size": 16,
                },
            },
        },
        "scales": {
            "y": {
                "beginAtZero": True,
                "display": chart_type in ["bar", "line"],
                "title": {
                    "display": True,
                    "text": y_axis_title,
                    "font": {
                        "size": 14,
                    },
                },
            },
            "x": {
                "display": True,
                "title": {
                    "display": True,
                    "text": x_axis_title,
                    "font": {
                        "size": 14,
                    },
                },
            },
        },
        **({"cutoutPercentage": 60} if chart_type == "doughnut" else {}),
    }
    options_json = json.dumps(options)

    js_code = """
    function createChart(chartData, chartOptions, canvasId) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        new Chart(ctx, {
            type: chartData.type,
            data: chartData.data,
            options: chartOptions
        });
    }
    """

    component_html = f"""
    <canvas id='{canvas_id}' width='{canvas_width}' height='{canvas_height}'></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        {js_code}
        createChart({{'type': '{chart_type}', 'data': {data_json}}}, {options_json}, '{canvas_id}');
    </script>
    """

    iframe_height = canvas_height + 50  # Add some extra space for padding
    components.html(component_html, height=iframe_height)


# Use this function in your Streamlit app, specifying canvas_width and canvas_height if needed
