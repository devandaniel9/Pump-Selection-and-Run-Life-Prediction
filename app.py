import pickle
import pandas as pd

from formula import *
from util import *

import streamlit as st

import plotly.graph_objects as go

#st.title("Pump Selection and Run Life Prediction")
new_title = '<p style="font-family:Segoe UI ; color:Black; font-size: 36px;"><b>Pump Selection and Run Life Prediction</b></p>'
st.markdown(new_title, unsafe_allow_html=True)

st.sidebar.subheader("Well Information")
platform                = st.sidebar.selectbox("Platform:  ",platforms_arr)
well                    = st.sidebar.selectbox("Well:  ",wells_arr)
vendor                  = st.sidebar.selectbox("Vendor :  ",vendors_arr)
problems                = st.sidebar.selectbox("Problems:  ",problems_arr)

st.sidebar.subheader("Well Performance")
liquid_rate             = st.sidebar.number_input('Liquid Rate',value=1000)
water_cut               = st.sidebar.number_input('Water Cut',value=91)
tubing_head_pressure    = st.sidebar.number_input('Tubing Head Pressure',value=700)
casing_head_pressure    = st.sidebar.number_input('Casing Head Pressure',value=170)
sbhp                    = st.sidebar.number_input('SBHP',value=1253)
fbhp                    = st.sidebar.number_input('FBHP',value=420)
st.sidebar.subheader("Completion Data")
casing_id               = st.sidebar.number_input('Casing ID',value=6.3)
pump_setting_depth      = st.sidebar.number_input('Pump Setting Depth',value=6962)
tubing_od               = st.sidebar.number_input('Tubing OD',value=2.875)
tubing_id               = st.sidebar.number_input('Tubing ID',value=2.441)
tlpsd                   = st.sidebar.number_input('Tubing Length to PSD',value=6901.4)
perforation_depth       = st.sidebar.number_input('Perforation Depth',value=6994)
gas_rate                = st.sidebar.number_input('Gas Rate',value=481)
st.sidebar.subheader("Fluid Properties")
sg_oil                  = st.sidebar.number_input('SG Oil',value=0.892)
sg_gas                  = st.sidebar.number_input('SG Gas',value=0.65)
sg_water                = st.sidebar.number_input('SG Water',value=1.05)
formation_volume_factor_water = st.sidebar.number_input('Formation Volume Factor Water',value=1)
temperature_suction     = st.sidebar.number_input('Temperature Suction',value=244)
interfacial_tension     = st.sidebar.number_input('Interfacial Tension',value=0.04)
acceleration_of_gravity = st.sidebar.number_input('Acceleration of Gravity',value=32)
st.sidebar.subheader("Further Details")
ipr_equation            = st.sidebar.selectbox('IPR Equation',['vogel','fetkovich','wiggins'])
desired_q               = st.sidebar.number_input('Desired Q',value=500)


# Well Performance Data
p_res = p_reservoir(perforation_depth, pump_setting_depth, water_cut, sg_oil, sg_water, sbhp)
p_wf = pwf(perforation_depth, pump_setting_depth, water_cut, sg_oil, sg_water, fbhp)
gor = gasoil_rate(gas_rate, desired_q, water_cut)
wor = wateroil_rate(desired_q, water_cut)

# Completion Data
f_loss = frictional_loss(desired_q, tubing_id)

# Fluid Properties
t_rankine = tempsuction_rankine(temperature_suction)    

# Well Performance
pres_arr = [p_res]
q_arr = [0]
diff = int(p_res/15)
curr = p_res
for i in range(15):
    curr -= diff
    pres_arr.append(curr)

if ipr_equation == 'vogel':
    q_vog = q_vogel(liquid_rate, p_wf, p_res)
    for el in pres_arr[1:]:
        qvog_ipr = qvogel_ipr(q_vog, el, p_res)
        q_arr.append(int(qvog_ipr))
elif ipr_equation == 'fetkovich':
    q_fet = q_fetkovich(liquid_rate, p_wf, p_res)
    for el in pres_arr[1:]:
        qfet_ipr = qfetkovich_ipr(q_fet, el, p_res)
        q_arr.append(int(qfet_ipr))
elif ipr_equation == 'wiggins':
    q_wig = q_wiggins(liquid_rate, p_wf, p_res)
    for el in pres_arr[1:]:
        qwig_ipr = qwiggins_ipr(q_wig, el, p_res)
        q_arr.append(int(qwig_ipr))

fbhp_dq = fbhpipr(desired_q, pres_arr, q_arr)

# Turpin Function
sg_liq = sg_liquid(water_cut, sg_oil, sg_water)
#st.write("sg_liq", sg_liq)
liquid_grad = liquid_gradient(sg_liq)
#st.write("liquid_grad", liquid_grad)
intake_pressure_turpin = pump_intake(p_wf, perforation_depth, pump_setting_depth, liquid_grad)
#st.write("intake_pressure_turpin", intake_pressure_turpin)
api_turpin = APIturpin(sg_oil)
#st.write("api_turpin", api_turpin)
yturpin = y_turpin(temperature_suction, api_turpin)
#st.write("yturpin", yturpin)
rsturpin = Rs_turpin(sg_gas, intake_pressure_turpin, yturpin)
#st.write("rsturpin", rsturpin)
oilrateturpin = OilRate_Turpin(liquid_rate, water_cut)
#st.write("oilrateturpin", oilrateturpin)
ppcturpin = Ppc_turpin(sg_gas)
#st.write("ppcturpin", ppcturpin)
tpcturpin = Tpc_turpin(sg_gas)
#st.write("tpcturpin", tpcturpin)
pprturpin = Ppr_turpin(intake_pressure_turpin, ppcturpin)
#st.write("pprturpin", pprturpin)
tprturpin = Tpr_turpin(t_rankine, tpcturpin)
#st.write("tprturpin", tprturpin)
zturpin = Z_turpin(pprturpin, tprturpin)
#st.write("zturpin", zturpin)
bgturpin = Bg_Turpin(t_rankine, intake_pressure_turpin, zturpin)
#st.write("bgturpin", bgturpin)
insiturate = InsituGasRate(gor, rsturpin, oilrateturpin, bgturpin)
#st.write("insiturate", insiturate)
fturpin = F_turpin(sg_oil, sg_gas, temperature_suction, rsturpin)
#st.write("fturpin", fturpin)
boturpin = Bo_turpin(fturpin)
#st.write("boturpin", boturpin)
gasdensity = gas_density(sg_gas, bgturpin)
#st.write("gasdensity", gasdensity)
liqdensity = liq_density(wor, sg_oil, sg_water, formation_volume_factor_water, boturpin)
#st.write("liqdensity", liqdensity)
Aturpin = A_turpin(casing_id, tubing_od)
#st.write("Aturpin", Aturpin)
Vbturpin = Vb_turpin(interfacial_tension, acceleration_of_gravity, gasdensity, liqdensity)
#st.write("Vbturpin", Vbturpin)
Vslturpin = Vsl_turpin(wor, formation_volume_factor_water, desired_q, boturpin, Aturpin)
#st.write("Vslturpin", Vslturpin)
natural_eff = naturalgas_eff(Vbturpin, Vslturpin)
#st.write("natural_eff", natural_eff)
ingestedgas = ingested_gas(insiturate, natural_eff)
#st.write("ingestedgas", ingestedgas)
qpumpturpin = Qpump_turpin(rsturpin, ingestedgas)
#st.write("qpumpturpin", qpumpturpin)
qlpumpturpin = qlpump_turpin(wor, formation_volume_factor_water, oilrateturpin, boturpin)
#st.write("qlpumpturpin", qlpumpturpin)
totalpumpfluid = totalfluid_pump (ingestedgas, qlpumpturpin)
#st.write("totalpumpfluid", totalpumpfluid)
turpin_func = turpin_parameter(intake_pressure_turpin, ingestedgas, qlpumpturpin)

if turpin_func > 1:
    turpin_det = 'Need Gas Separator'
else:
    turpin_det = 'No Need Gas Separator'
#st.write("turpin_func", turpin_func)

# Get pumps within desired q
pumps_arr = get_pumps(desired_q)

# Create model input
data = get_model_input_arr(desired_q, problems, pumps_arr, platform, well, vendor)

# Load Model
with open('../model/model.sav', 'rb') as file :
    model = pickle.load(file)

# Predict
preds = []
for i in range(len(data)):
    predict = model.predict(data[i].reshape(1,-1))
    efficiency = pump_efficiency(pumps_arr[i], desired_q)
    hpstages = pump_hpstages(pumps_arr[i], desired_q)
    headstages = pump_headstages(pumps_arr[i], desired_q)
    
    # Pump intake pressure
    sg_liq = sg_liquid(water_cut, sg_oil, sg_water)
    liquid_grad = liquid_gradient(sg_liq)
    intake_pressure = pump_intake(fbhp_dq, perforation_depth, pump_setting_depth, liquid_grad)
    
    # Dynamic liquid level
    oil_grad = oilgradient(sg_oil)
    dll = dynamicliquidlevel(pump_setting_depth, oil_grad, casing_head_pressure, intake_pressure)

    # Total dynamic head
    hfr = frictional_headloss(f_loss, tlpsd)
    tdh = totaldynamichead(hfr, dll, tubing_head_pressure, sg_liq)

    # Pump stages
    pump_stages = pumpstages(tdh, headstages)

    # Require pump power
    req_power = brake_hp(p_res, hpstages, liquid_grad)

    # BHPT
    bhpt = brake_hp_with_gas(req_power)

    temp = {
            "pump": pumps_arr[i], 
            "run_life": float("{:.2f}".format(predict.tolist()[0])),
            "efficiency": float("{:.2f}".format(efficiency)),
            "hp/stages": float("{:.2f}".format(hpstages)),
            "head/stages": float("{:.2f}".format(headstages)),
            "pump_intake_pressure": float("{:.2f}".format(intake_pressure)),
            "dynamic_liq_level": float("{:.2f}".format(dll)),
            "total_dynamic_head": float("{:.2f}".format(tdh)),
            "num_of_stages": float("{:.2f}".format(pump_stages)),
            "req_pump_power": float("{:.2f}".format(req_power)),
            "bhpt": float("{:.2f}".format(bhpt))
        }
    preds.append(temp)


p_reservoir = p_res
pwf = p_wf
gor = gor
wor = wor
frictional_headloss = f_loss
temp_suction = t_rankine
ipr_equation = ipr_equation
p_res_arr = pres_arr
q_arr = q_arr
fbhp_dq = fbhp_dq
desired_q = desired_q
turpin_func = turpin_func
predictions = preds

#Table 1
data1 = [['Pres', round(p_res,2),'psi'], 
        ['Pwf', round(pwf,2),'psi'], 
        ['GOR', round(gor,2), 'scf/bbl'],
        ['WOR', wor, 'scf/bbl']
]

df = pd.DataFrame(data1,columns = ['Well Performance Data', '', ' '])
fig = go.Figure(data=[go.Table(
    columnwidth=[0.7,0.5,0.3],
    header=dict(
        values=["<b><i>Well Performance Data<i><b>", "", " "],
        line_color='#B1D0E4', fill_color='#B1D0E4',
        align='left', font=dict(color='black', size=17)
    ),
    cells=dict(
        values=[df['Well Performance Data'], df[''], df[' ']],
        line_color='white', fill_color='white',
        align='left', font=dict(color='black', size=14),
        height = 30
  ))
])
fig.update_layout(width=1000,height = 150, margin=dict(l=0,r=0,b=0,t=0))
st.write(fig)
st.write('')


#Table2
data2 = [['Frictional Headloss', round(frictional_headloss,2),'ft/1000ft']]
df2 = pd.DataFrame(data2,columns = ['Completion Data', '', ' '])
fig2 = go.Figure(data=[go.Table(
    columnwidth=[0.7,0.5,0.3],
    header=dict(
        values=["<b><i>Completion Data<i><b>", "", " "],
        line_color='#B1D0E4', fill_color='#B1D0E4',
        align='left', font=dict(color='black', size=17)
    ),
    cells=dict(
        values=[df2['Completion Data'], df2[''], df2[' ']],
        line_color='white', fill_color='white',
        align='left', font=dict(color='black', size=14),
        height = 30
  )) 
])
fig2.update_layout(width=1000,height = 70, margin=dict(l=0,r=0,b=0,t=0))
st.write(fig2)

#Table 3
data3 = [['Fluid Properties', round(temp_suction,2),'R']]
df3= pd.DataFrame(data3,columns = ['Temperature Suction', '', ' '])
fig3 = go.Figure(data=[go.Table(
    columnwidth=[0.7,0.5,0.3],
    header=dict(
        values=["<b><i>Temperature Suction<i><b>", "", " "],
        line_color='#B1D0E4', fill_color='#B1D0E4',
        align='left', font=dict(color='black', size=17)
    ),
    cells=dict(
        values=[df3['Temperature Suction'], df3[''], df3[' ']],
        line_color='white', fill_color='white',
        align='left', font=dict(color='black', size=14),
        height = 30
  )) 
])

fig3.update_layout(width=1000,height = 70, margin=dict(l=0,r=0,b=0,t=0))
st.write(fig3)

#Chart
plot_df = pd.DataFrame({'pwf':p_res_arr,'q':q_arr})
c = go.Figure()
c.add_trace(go.Scatter(x=plot_df.q, y=plot_df.pwf,
                    #mode='lines',
                    name=ipr_equation.title(),
                    line=dict(width=3, color='#516e94'),
                    fill='tozeroy',
                    opacity=0.5,
                    ))

c.add_trace(go.Scatter(x=[0,0,desired_q,desired_q], y=[0,fbhp_dq,fbhp_dq,0],
                    #mode='lines',
                    name='FBHP @ Desired Q',
                    line=dict(width=1, color='#32445c'),
                    fill='tozeroy',
                    opacity=0.5,
                    ))

c.update_layout(
                   xaxis_title="Liquid Rate, STB/D",
                   yaxis_title="Bottom Hole Pressure, psi",
                   width = 1000,
                   height = 600,
                   margin=dict(l=0,r=0,b=0,t=10),
                   legend=dict(
                            yanchor="top",
                            y= 0.93,
                            xanchor="right",
                            x=0.97,
                            bgcolor='LightSteelBlue',
                            bordercolor="Black",
                            borderwidth=1
                            )
                   
                   )
             
st.plotly_chart(c)

data4 = [   ['FBHP @ Desired Q', round(fbhp_dq,2),'psi'],
            ['Turpin Function', round(turpin_func,2),turpin_det]]
df4= pd.DataFrame(data4,columns = ['Well Performance', '', ' '])
fig4 = go.Figure(data=[go.Table(
    columnwidth=[0.7,0.5,0.3],
    header=dict(
        values=["<b><i>Well Performance<i><b>", "", " "],
        line_color='#B1D0E4', fill_color='#B1D0E4',
        align='left', font=dict(color='black', size=17)
    ),
    cells=dict(
        values=[df4['Well Performance'], df4[''], df4[' ']],
        line_color='white', fill_color='white',
        align='left', font=dict(color='black', size=14),
        height = 30
  )) 
])

fig4.update_layout(width=1000,height = 120, margin=dict(l=0,r=0,b=0,t=0))

st.write(fig4)

data5 = [   ['Pump'                 , preds[0]['pump']                          ,''],
            ['Run Life'             , round(preds[0]['run_life'],2)             ,'days'],
            ['Efficiency'           , round(preds[0]['efficiency'],2)           ,'%'],
            ['HP/Stages'            , round(preds[0]['hp/stages'],2)            ,'HP/stage'],
            ['Head/Stages'          , round(preds[0]['head/stages'],2)          ,'ft/stage'],
            ['Pump Intake Pressure' , round(preds[0]['pump_intake_pressure'],2) ,'psi'],
            ['Dynamic Liquid Level' , round(preds[0]['dynamic_liq_level'],2)    ,'ft/stage'],
            ['Total Dynamic Head'   , round(preds[0]['total_dynamic_head'],2)   ,'ft/stage'],
            ['Number of Stages'     , round(preds[0]['num_of_stages'],2)        ,'stages'],
            ['Required Pump Power'  , round(preds[0]['req_pump_power'],2)       ,'HP'],
            ['BHPT'                 , round(preds[0]['bhpt'],2)                 ,'HP'],
]

df5= pd.DataFrame(data5,columns = ['Recommendation 1', '', ' '])
fig5 = go.Figure(data=[go.Table(
    columnwidth=[0.7,0.5,0.3],
    header=dict(
        values=["<b><i>Recommendation 1<i><b>", "", " "],
        line_color='#B1D0E4', fill_color='#B1D0E4',
        align='left', font=dict(color='black', size=17)
    ),
    cells=dict(
        values=[df5['Recommendation 1'], df5[''], df5[' ']],
        line_color='white', fill_color='white',
        align='left', font=dict(color='black', size=14),
        height = 30
  )) 
])

fig5.update_layout(width=1000, height = 400, margin=dict(l=0,r=0,b=0,t=0))

st.write(fig5)

data6 = [   ['Pump'                 , preds[1]['pump']                          ,''],
            ['Run Life'             , round(preds[1]['run_life'],2)             ,'days'],
            ['Efficiency'           , round(preds[1]['efficiency'],2)           ,'%'],
            ['HP/Stages'            , round(preds[1]['hp/stages'],2)            ,'HP/stage'],
            ['Head/Stages'          , round(preds[1]['head/stages'],2)          ,'ft/stage'],
            ['Pump Intake Pressure' , round(preds[1]['pump_intake_pressure'],2) ,'psi'],
            ['Dynamic Liquid Level' , round(preds[1]['dynamic_liq_level'],2)    ,'ft/stage'],
            ['Total Dynamic Head'   , round(preds[1]['total_dynamic_head'],2)   ,'ft/stage'],
            ['Number of Stages'     , round(preds[1]['num_of_stages'],2)        ,'stages'],
            ['Required Pump Power'  , round(preds[1]['req_pump_power'],2)       ,'HP'],
            ['BHPT'                 , round(preds[1]['bhpt'],2)                 ,'HP'],
]

df6= pd.DataFrame(data6,columns = ['Recommendation 2', '', ' '])
fig6 = go.Figure(data=[go.Table(
    columnwidth=[0.7,0.5,0.3],
    header=dict(
        values=["<b><i>Recommendation 2<i><b>", "", " "],
        line_color='#B1D0E4', fill_color='#B1D0E4',
        align='left', font=dict(color='black', size=17)
    ),
    cells=dict(
        values=[df6['Recommendation 2'], df6[''], df6[' ']],
        line_color='white', fill_color='white',
        align='left', font=dict(color='black', size=14),
        height = 30
  )) 
])

fig6.update_layout(width=1000, height = 400, margin=dict(l=0,r=0,b=0,t=0))

st.write(fig6)
