# 接下来要学习一个新的三方库叫做Gradio。
# 之所以要学Gradio，是因为我们在前面项目里面用前后端的方式去做展示的时候，有同学反馈说没有前后端基础，学完还是一知半解。
# 所以在这个项目中，我们借助Gradio用Python的方式来搭建这个展示界面。

# Gradio是什么
# Gradio是一个开源的Python库，用于快速构建一个简单漂亮的用户界面，以便向客户、合作者、用户或学生展示机器学习模型。
# 大家注意，前面介绍中的有一个词叫做展示，所以在商业项目中一般还是会用前后端的方式去做交互，Gradio只是方便我们学习和调试的。
# 另外说明一点，这个库可以做对话、图片生成等很多场景的交互，但我们这个项目当中只有对话的场景，所以课上只讲项目需要用到的，其他场景在后面遇到了在做补充。
# 简单理解，就是把它当做工具使用，需要什么就去文档查看即可。

# https://www.gradio.app/

# 1.安装Gradio
# pip install gradio

# 2.初体验
import gradio as gr

# 快速上手
def greet(name):
    return '你好 ' + name

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
# if __name__ == '__main__':
#     demo.launch(share=True)

# 3.修改属性
demo = gr.Interface(
    fn=greet,
    inputs=[gr.Text(label='姓名', value='陈华编程', lines=5)],
    outputs=[gr.Text(label='输出', lines=5)]
)

if __name__ == '__main__':
    demo.launch()

# 通过这个简单例子，我们了解了Text这个组件的用法。其实这个库，本质上还是生成了前端的html代码，只是可以用Python的格式去书写。
# 其他组件还有很多，这种工具类的库，大家也不用背记，需要的时候去官网复制就可以了。
# 下节课，我们就直奔主题，直接去布局对话的窗口页面。
