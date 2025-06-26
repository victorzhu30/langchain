from langchain import hub

# 拉取模板
prompt = hub.pull("hwchase17/openai-tools-agent")
print(prompt.messages)
# [SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='You are a helpful assistant'), additional_kwargs={}), 
# MessagesPlaceholder(variable_name='chat_history', optional=True), 
# HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], input_types={}, partial_variables={}, template='{input}'), additional_kwargs={}), 
# MessagesPlaceholder(variable_name='agent_scratchpad')]

# 打印对象的类型，你会看到它是 ChatPromptTemplate
print(f"Prompt 类型: {type(prompt)}\n")

# 遍历并打印每个消息模板的内容
print("--- ChatPromptTemplate 的详细结构 ---")
for message_template in prompt.messages:
    # 打印每个消息模板的类型
    print(f"消息类型: {type(message_template)}")
    
    # 不同的消息模板有不同的结构，我们分别处理
    if hasattr(message_template, 'prompt'):
        # 对于 SystemMessagePromptTemplate 和 HumanMessagePromptTemplate
        print(f"  - 模板内容: {message_template.prompt.template}")
        print(f"  - 输入变量: {message_template.prompt.input_variables}")
    elif hasattr(message_template, 'variable_name'):
        # 对于 MessagesPlaceholder
        print(f"  - 占位符变量名: {message_template.variable_name}")
    print("-" * 20)

# System Message: 这是给 LLM 的核心指令，告诉它它的角色（"a helpful assistant"）、它有哪些工具可用（{tools}）、以及它必须遵循的思考-行动-观察的格式。
# chat_history Placeholder: 这是一个占位符，用于在对话中插入之前的聊天记录，让 Agent 拥有记忆。
# Human Message: 这就是用户的输入。它的模板是 {input}，这正是为什么你在调用 .invoke 时必须使用 {'input': ...} 的原因。
# agent_scratchpad Placeholder: 这是一个非常关键的占位符。Agent 在思考过程中（比如调用工具、看到观察结果）的所有中间步骤都会被填充到这里。这使得 LLM 在下一步决策时，能看到自己之前的“草稿”或“思考链”。