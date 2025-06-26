# 上节课当中，简单体验了一下Gradio的基本用法，用几行简单的代码，就可以实现一个交互界面。
# 因为比较简单，其他组件就不挨个讲了，大家需要的时候，去看一眼文档就可以了。
# 这节课我们要布局的是一个对话的界面，因为是一个常用的场景，所以Gradio做好了封装，直接调就可以了。
# https://www.gradio.app/docs/gradio/chatinterface

import gradio as gr

def echo(message, history):
    return message

# 界面限宽
css = '''
.gradio-container {max-width: 850px !important; margin: 20px auto !important;}
.message {padding: 19px !important; font-size: 14px !important}
'''

demo = gr.ChatInterface(
    css=css,
    fn=echo, 
    type="messages", 
    examples=["hello", "hola", "merhaba"], 
    title="Echo Bot")

if __name__ == '__main__':
    demo.launch()