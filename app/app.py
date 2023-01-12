import gradio as gr
import hopsworks

project = hopsworks.login()

dataset_api = project.get_dataset_api()

dataset_api.download("Resources/aqi/images/df_next_7_days.png", overwrite=True)


def update():
    dataset_api.download("Resources/aqi/images/df_next_7_days.png", overwrite=True)
    return "df_next_7_days.png"


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Label("Paris - AQI Predictions")
            gr.Button("Update Predictions").click(update, None, gr.Image("df_next_7_days.png"))

demo.launch()
