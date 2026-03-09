from langgraph.graph import StateGraph, START, END
from typing import TypedDict
class BMI_state(TypedDict):
    BMI_height:float
    BMI_weight:float
    BMI:float
    BMI_label: str
def BMI_calculator(state:BMI_state)->BMI_state:
    h=state['BMI_height']
    w=state['BMI_weight']
    state['BMI']=round(w/(h**2), 2) #partial update in state
    return state
def bmi_label(state:BMI_state)->BMI_state:
    bmi=state['BMI']
    if(bmi<=25):
        state['BMI_label']='fit'
    elif(bmi<=30):
        state['BMI_label']='overweight'
    else:
        state['BMI_label']="obese"
    return state

graph= StateGraph(BMI_state)
#create the node
graph.add_node('calculate_BMI',BMI_calculator)
graph.add_node('label_BMI',bmi_label)

#add the edges
graph.add_edge(START,'calculate_BMI') #start--->Calculate_BMI--->end
graph.add_edge('calculate_BMI','label_BMI')
graph.add_edge('label_BMI',END)
#compile
workflow=graph.compile()

#invoke
inital_state={'BMI_height':1.80, 'BMI_weight':80}
final_state=workflow.invoke(inital_state)
print(final_state)

#save the graph
with open("graph.png", "wb") as f:
    f.write(workflow.get_graph().draw_mermaid_png())