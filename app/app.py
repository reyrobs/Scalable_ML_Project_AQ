import gradio as gr
import hopsworks

project = hopsworks.login()
fs = project.get_feature_store()

dataset_api = project.get_dataset_api()

dataset_api.download("Resources/aqi/images/df_next_7_days.png")

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Label("Paris - AQI Predictions for the Next 7 Days")
            input_img = gr.Image("df_next_7_days.png", elem_id="predicted-img")

demo.launch()
