import numpy as np

def p_reservoir(pd, psd, wc, sg_oil, sg_water, sbhp):
    p_res = (pd - psd) * ((1 - (wc / 100 * sg_oil)) + (wc / 100 * sg_water) * 0.433) + sbhp
    return p_res

def pwf(pd, psd, wc, sg_oil, sg_water, fbhp):
    p_wf = (pd - psd) * ((1 - (wc / 100 * sg_oil)) + (wc / 100 *sg_water) * 0.433) + fbhp
    return p_wf

def gasoil_rate(gas_rate, desired_q, wc):
    gor = gas_rate / ( desired_q - (desired_q * wc / 100)) * 1000
    return gor

def wateroil_rate(desired_q, wc):
    wor = (desired_q - (desired_q * wc/100)) / (desired_q * (100 - wc) / 100)
    return wor

def frictional_loss(desired_q, tubing_id):
    fricloss_hazenwill = (2.083 * ((100 / 120)**1.852) * ((desired_q / 34.3)**1.85)) / (tubing_id**4.8655)
    return fricloss_hazenwill

def tempsuction_rankine(temp_suction):
    tempsuct_rankine = (temp_suction + 460)
    return tempsuct_rankine

def pressure_ipr(p_res): #ini pres nya yang dibagi 15, tapi kan nanti gerak kebawah p_res nya, jadi nilainya ganti ganti nanti makin kebawah. nilai p_res yang tetep cuman p_res yang di rumus (p_res/15)
    press_ipr = p_res - (p_res/15)
    return press_ipr

def q_vogel(liquid_rate, p_wf, p_res):
    q_vog = liquid_rate / (1-0.2*(p_wf/p_res)-0.8*(p_wf/p_res)**2)
    return q_vog

def q_fetkovich(liquid_rate, p_wf, p_res):
    q_fet = liquid_rate / ((p_res**2) - (p_wf**2))
    return q_fet

def q_wiggins(liquid_rate, p_wf, p_res):
    q_wig = liquid_rate / (1-0.52*(p_wf/p_res)-0.48*(p_wf/p_res)**2)
    return q_wig

def qvogel_ipr(q_vog, p_wf, p_res): #ini pwf sama pres nya yang dibagi 15
    qvog_ipr = q_vog * (1-0.2*(p_wf/p_res)-0.8*(p_wf/p_res)**2)
    return qvog_ipr

def qfetkovich_ipr(q_fet, p_wf, p_res): #ini pwf sama pres nya yang dibagi 15
    qfet_ipr = q_fet * ((p_res**2) - (p_wf**2))
    return qfet_ipr

def qwiggins_ipr(q_wig, p_wf, p_res): #ini pwf sama pres nya yang dibagi 15
    qwig_ipr = q_wig * (1-0.52*(p_wf/p_res)-0.48*(p_wf/p_res)**2)
    return qwig_ipr

def fbhp_const(x,y):
    x = np.array(x)
    y = np.array(y)
    const_arr = np.polyfit(y, x, deg=4)
    return const_arr

def fbhpipr(desired_q, x, y): #ini aslinya ada konstantanya fizh, konstantanya berubah2 sesuai pilihan ipr equation
    const_arr = fbhp_const(x,y)
    fbhp_ipr = (const_arr[0]*(desired_q**4)) + (const_arr[1]*(desired_q**3)) + (const_arr[2]*(desired_q**2)) + (const_arr[3]*desired_q) + const_arr[4]
    return fbhp_ipr

#turpin parameter

def sg_liquid (wc, sg_oil, sg_water):
    SG_liquid = ((1-(wc/100))*sg_oil)+((wc/100)*sg_water)
    return SG_liquid

def liquid_gradient (SG_liquid):
    liq_grad = SG_liquid * 0.433
    return liq_grad

def pump_intake (fbhp_ipr, pd, psd, liq_grad):
    PIP = fbhp_ipr - ((pd - psd)*liq_grad)
    return PIP

def APIturpin (sg_oil):
    API = (141.5/sg_oil) - 131.5
    return API

def y_turpin (temp_suction, API):
    y = (0.00091*temp_suction)-(0.01215*API)
    return y

def Rs_turpin (sg_gas, PIP, y):
    Rs = (sg_gas*((PIP/18*(10**y)))**1.205)
    return Rs

def OilRate_Turpin (liquid_rate, wc):
    print("func oilrate_turpin", liquid_rate, wc)
    OilRate = (1-(wc/100))*liquid_rate
    return OilRate

def Ppc_turpin (sg_gas):
    ppc = (709.6-(58.7*sg_gas))
    return ppc

def Tpc_turpin (sg_gas):
    tpc = (170.5+(307.3*sg_gas))
    return tpc

def Ppr_turpin (pip, ppc):
    ppr = pip/ppc
    return ppr

def Tpr_turpin (tempsuct_rankine, tpc):
    tpr = tempsuct_rankine/tpc
    return tpr

def Z_turpin (ppr, tpr):
    Z = (1-((3.52 * ppr)/(10**(0.9813 * tpr)))+((0.274*(ppr**2))/(10**(0.8157*tpr))))
    return Z

def Bg_Turpin (tempsuct_rankine, PIP, Z ):
    Bg = (0.0283*((Z*tempsuct_rankine)/PIP))
    return Bg

def InsituGasRate (gor, Rs, OilRate, Bg):
    qginsitu = (OilRate*(gor-Rs)*Bg)
    return qginsitu

def F_turpin (sg_oil, sg_gas, temp_suction, Rs):
    F = (Rs*((sg_gas/sg_oil)**0.5))+1.25*temp_suction
    return F

def Bo_turpin (F):
    Bo = (0.972+((1.47*(10**-4))*(F**1.175)))
    return Bo

def gas_density (sg_gas, Bg):
    rho_g = (0.0764*sg_gas)/Bg
    return rho_g

def liq_density (wor, sg_oil, sg_water, bw, Bo):
    rho_l =(62.4*(((sg_oil/Bo)*(1/(1+wor)))+((sg_water/bw)*(wor/(1+wor)))))
    return rho_l

def A_turpin (casing_id, tubing_od):
    A = (0.0055*((casing_id**2)-(tubing_od**2)))
    return A

def Vb_turpin (ift, acceleration_gravity, rho_g, rho_l):
    Vb = ((2**(1/2))*((ift*acceleration_gravity*(rho_l-rho_g))/(rho_l**2))**(1/4))
    return Vb

def Vsl_turpin (wor, fvf, desired_q, Bo, A):
    Vsl =((6.5*(10**-5))*((desired_q/A)*((Bo/(1+wor))+(fvf*(wor/(1+wor))))))
    return Vsl

def naturalgas_eff (Vb, Vsl):
    EffNatural = (Vb/(Vb+Vsl))*100
    return EffNatural

def ingested_gas (qginsitu, EffNatural):
    qing = (qginsitu/5.61)*(1-(EffNatural/100))
    return qing

def Qpump_turpin (Rs, qing):
    qpump = (qing + Rs)
    return qpump

def qlpump_turpin (wor, fvf, OilRate, Bo):
    qlpump = (OilRate*(Bo+(fvf*wor)))
    return qlpump

def totalfluid_pump (qing, qlpump):
    qt = qing + qlpump
    return qt

def turpin_parameter (PIP, qing, qlpump):
    turpin = ((2000*(qing/qlpump))/(3*PIP))
    return turpin

#Formula for each Pump:
# 1. Efficiency

def pump_efficiency(pump, desired_q):
    if pump == 'RC1000':
        RC1000_eff = 0.000000000000000000140546398107*desired_q**6 - 0.000000000000000878790942453078*desired_q**5 + 0.000000000001759325373441020000*desired_q**4 - 0.000000001252087946778530000000*desired_q**3 - 0.000000665270605743062000000000*desired_q**2 + 0.001580333126426580000000000000*desired_q + 0.000001420841194033070000000000
        return RC1000_eff
    elif pump == 'Q08':
        Q08_eff = 0.000000000000000000165883099790*desired_q**6 - 0.000000000000001124451875252020*desired_q**5 + 0.000000000002548942779756570000*desired_q**4 - 0.000000002486320158030840000000*desired_q**3 + 0.000000060463410389566300000000*desired_q**2 + 0.001283081846047200000000000000*desired_q + 0.000233704643839872000000000000
        return Q08_eff
    elif pump == 'Q10':
        Q10_eff = -0.000000000000000000099917465192*desired_q**6 + 0.000000000000000777753424370859*desired_q**5 - 0.000000000002199056775992630000*desired_q**4 + 0.000000002600780108310590000000*desired_q**3 - 0.000001862230248284020000000000*desired_q**2 + 0.001383515571398600000000000000*desired_q - 0.000096750222844832500000000000
        return Q10_eff
    elif pump == 'Q20':
        Q20_eff = -0.000000000000000000002783619890*desired_q**6 + 0.000000000000000038361980507080*desired_q**5 - 0.000000000000198349413707152000*desired_q**4 + 0.000000000399408055369273000000*desired_q**3 - 0.000000515649973126947000000000*desired_q**2 + 0.000786503588243725000000000000*desired_q - 0.000281365912286446000000000000
        return Q20_eff
    elif pump == 'DN1750':
        DN1750_eff = 0.000000000000000000029458827602*desired_q**6 - 0.000000000000000230193191835447*desired_q**5 + 0.000000000000651673304933743000*desired_q**4 - 0.000000000795747123250902000000*desired_q**3 + 0.000000141804475384255000000000*desired_q**2 + 0.000761577263714841000000000000*desired_q + 0.000154004717416001000000000000
        return DN1750_eff
    elif pump == 'QN55':
        QN55_eff = 0.000000000000000000000013373395*desired_q**6 - 0.000000000000000000303377145705*desired_q**5 + 0.000000000000001926303395929070*desired_q**4 - 0.000000000002506472656439680000*desired_q**3 - 0.000000045162886173032200000000*desired_q**2 + 0.000325170140652808000000000000*desired_q - 0.000372554815683657000000000000
        return QN55_eff
    elif pump == 'SN3600':
        SN3600_eff = 0.000000000000000000000002442733*desired_q**6 - 0.000000000000000000705766864932*desired_q**5 + 0.000000000000006528092586372040*desired_q**4 - 0.000000000019814822666439600000*desired_q**3 - 0.000000038895692080348500000000*desired_q**2 + 0.000403220272643168000000000000*desired_q + 0.000025176279052630000000000000
        return SN3600_eff
    elif pump == 'QN70':
        QN70_eff = 0.000000000000000000000001167537*desired_q**6 - 0.000000000000000000274827064664*desired_q**5 + 0.000000000000004593506281278870*desired_q**4 - 0.000000000027266697937800500000*desired_q**3 + 0.000000041248297005021900000000*desired_q**2 + 0.000206682375453404000000000000*desired_q + 0.000877189973763848000000000000
        return QN70_eff
    elif pump == 'QN120':
        QN120_eff = -0.000000000000000000000000043827*desired_q**6 + 0.000000000000000000005736402457*desired_q**5 - 0.000000000000000184072752667037*desired_q**4 + 0.000000000002058246627990120000*desired_q**3 - 0.000000015611444685158900000000*desired_q**2 + 0.000150476438044445000000000000*desired_q - 0.000092079057218086300000000000
        return QN120_eff
    elif pump == 'QM200':
        QM200_eff = -0.000000000000000000000000079621*desired_q**6 + 0.000000000000000000006089850598*desired_q**5 - 0.000000000000000190180243082563*desired_q**4 + 0.000000000002933477522574850000*desired_q**3 - 0.000000025260972465690100000000*desired_q**2 + 0.000167545949438459000000000000*desired_q + 0.006654921040683060000000000000
        return QM200_eff
    elif pump == 'QM265':
        QM265_eff = -0.000000000000000000000000003320*desired_q**6 + 0.000000000000000000000271296720*desired_q**5 - 0.000000000000000008994192831965*desired_q**4 + 0.000000000000138099070286393000*desired_q**3 - 0.000000003269129309662530000000*desired_q**2 + 0.000087530949542165300000000000*desired_q + 0.035636544621433200000000000000
        return QM265_eff
    else:
        return None

# 2. HP/stages

def pump_hpstages(pump, desired_q):
    if pump == 'RC1000':
        RC1000_hpst = -0.000000000000000000393774833436*desired_q**6 + 0.000000000000002175551171866690*desired_q**5 - 0.000000000004487459000084340000*desired_q**4 + 0.000000004101932505359670000000*desired_q**3 - 0.000001496053538080360000000000*desired_q**2 + 0.000219717312450740000000000000*desired_q + 0.179997785265392000000000000000
        return RC1000_hpst
    elif pump == 'Q08':
        Q08_hpst = -0.000000000000000000167727162720*desired_q**6 + 0.000000000000001059688790630990*desired_q**5 - 0.000000000002240501244954320000*desired_q**4 + 0.000000001898774540430670000000*desired_q**3 - 0.000000535890536779160000000000*desired_q**2 + 0.000148436166419685000000000000*desired_q + 0.191796790036847000000000000000
        return Q08_hpst
    elif pump == 'Q10':
        Q10_hpst = 0.000000000000000000077172025950*desired_q**6 - 0.000000000000000506445325524745*desired_q**5 + 0.000000000001236085115624670000*desired_q**4 - 0.000000001378863331510680000000*desired_q**3 + 0.000000611506363462633000000000*desired_q**2 + 0.000119451852350849000000000000*desired_q + 0.207990127572316000000000000000
        return Q10_hpst
    elif pump == 'Q20':
        Q20_hpst = -0.000000000000000000000084352112*desired_q**6 - 0.000000000000000017186419507266*desired_q**5 + 0.000000000000114598729933788000*desired_q**4 - 0.000000000254799577473880000000*desired_q**3 + 0.000000203718322086544000000000*desired_q**2 + 0.000077418453683364400000000000*desired_q + 0.353784861688894000000000000000
        return Q20_hpst
    elif pump == 'DN1750':
        DN1750_hpst = -0.000000000000000000023439706151*desired_q**6 + 0.000000000000000222800518667461*desired_q**5 - 0.000000000000775440351530280000*desired_q**4 + 0.000000001203483143639970000000*desired_q**3 - 0.000000806699740237005000000000*desired_q**2 + 0.000223314568781774000000000000*desired_q + 0.279759935761106000000000000000
        return DN1750_hpst
    elif pump == 'QN55':
        QN55_hpst = -0.000000000000000000000008709413*desired_q**6 + 0.000000000000000000473252149313*desired_q**5 - 0.000000000000006048850607170460*desired_q**4 + 0.000000000025195335260743700000*desired_q**3 - 0.000000030058953288253400000000*desired_q**2 + 0.000087505929222686500000000000*desired_q + 1.300461393583130000000000000000
        return QN55_hpst
    elif pump == 'SN3600':
        SN3600_hpst = 0.000000000000000000000004413778*desired_q**6 + 0.000000000000000000335306696469*desired_q**5 - 0.000000000000002748933780783470*desired_q**4 - 0.000000000012452604085963600000*desired_q**3 + 0.000000104518588721347000000000*desired_q**2 + 0.000043647661655654700000000000*desired_q + 1.198844947103680000000000000000
        return SN3600_hpst
    elif pump == 'QN70':
        QN70_hpst = -0.000000000000000000000069530480*desired_q**6 + 0.000000000000000002043603415173*desired_q**5 - 0.000000000000021542903836979800*desired_q**4 + 0.000000000092915897489041200000*desired_q**3 - 0.000000128532711404783000000000*desired_q**2 - 0.000002780626198628510000000000*desired_q + 1.528588693118310000000000000000
        return QN70_hpst
    elif pump == 'QN120':
        QN120_hpst = -0.000000000000000000000001483374*desired_q**6 + 0.000000000000000000024646821446*desired_q**5 + 0.000000000000000129989161411156*desired_q**4 - 0.000000000003946597609187390000*desired_q**3 + 0.000000026489820940077400000000*desired_q**2 + 0.000005467900075828420000000000*desired_q + 2.154130944999000000000000000000
        return QN120_hpst
    elif pump == 'QM200':
        QM200_hpst = 0.000000000000000000000000002032*desired_q**6 - 0.000000000000000000000685547586*desired_q**5 - 0.000000000000000064364958019302*desired_q**4 + 0.000000000003322985812912400000*desired_q**3 - 0.000000057182118238041000000000*desired_q**2 + 0.000782276544602186000000000000*desired_q + 3.736408932934560000000000000000
        return QM200_hpst
    elif pump == 'QM265':
        QM265_hpst = 0.000000000000000000000000281233*desired_q**6 - 0.000000000000000000020808929599*desired_q**5 + 0.000000000000000549687949316022*desired_q**4 - 0.000000000006773825656199060000*desired_q**3 + 0.000000040853322626128300000000*desired_q**2 + 0.000289760029377356000000000000*desired_q + 7.093673697005500000000000000000
        return QM265_hpst
    else:
        return None

# 3. head/stages
def pump_headstages(pump, desired_q):
    if pump == 'RC1000':
        RC1000_hdst = 0.000000000000000001394456286426*desired_q**6 - 0.000000000000006053775678587910*desired_q**5 + 0.000000000010373203950539800000*desired_q**4 - 0.000000013413925734062600000000*desired_q**3 + 0.000000612574112324182000000000*desired_q**2 + 0.000919108565881288000000000000*desired_q + 33.500811326074200000000000000000
        return RC1000_hdst
    elif pump == 'Q08':
        Q08_hdst = 0.000000000000000015732996382436*desired_q**6 - 0.000000000000077569416134145400*desired_q**5 + 0.000000000147269358722322000000*desired_q**4 - 0.000000137204049065719000000000*desired_q**3 + 0.000042919945881791900000000000*desired_q**2 - 0.004752704221914430000000000000*desired_q + 35.137399184209500000000000000000
        return Q08_hdst
    elif pump == 'Q10':
        Q10_hdst = -0.000000000000000000947726635191*desired_q**6 + 0.000000000000008625770413956520*desired_q**5 - 0.000000000017687167025047200000*desired_q**4 + 0.000000001617615914481510000000*desired_q**3 + 0.000001018100296512610000000000*desired_q**2 + 0.000827842990617000000000000000*desired_q + 36.395277667773800000000000000000
        return Q10_hdst
    elif pump == 'Q20':
        Q20_hdst = -0.000000000000000000265709170337*desired_q**6 + 0.000000000000002214788130861920*desired_q**5 - 0.000000000007907014366726930000*desired_q**4 + 0.000000014133675289374300000000*desired_q**3 - 0.000017528880316475300000000000*desired_q**2 + 0.009569491049944650000000000000*desired_q + 32.757840387274400000000000000000
        return Q20_hdst
    elif pump == 'DN1750':
        DN1750_hdst = -0.000000000000000000163360114475*desired_q**6 + 0.000000000000003581640565738150*desired_q**5 - 0.000000000018418906000947300000*desired_q**4 + 0.000000037838577752417200000000*desired_q**3 - 0.000034909765667556800000000000*desired_q**2 + 0.006648321140346520000000000000*desired_q + 30.195405162383800000000000000000
        return DN1750_hdst
    elif pump == 'QN55':
        QN55_hdst = 0.000000000000000000000876538677*desired_q**6 - 0.000000000000000016208010751945*desired_q**5 + 0.000000000000108572790338650000*desired_q**4 - 0.000000000449566122962550000000*desired_q**3 + 0.000001185240708315160000000000*desired_q**2 - 0.006274702195028680000000000000*desired_q + 57.209230546868600000000000000000
        return QN55_hdst
    elif pump == 'SN3600':
        SN3600_hdst = 0.000000000000000000003714428389*desired_q**6 - 0.000000000000000067964359111099*desired_q**5 + 0.000000000000419851590789746000*desired_q**4 - 0.000000001343640416810730000000*desired_q**3 + 0.000000820903065190670000000000*desired_q**2 - 0.000089097552631756100000000000*desired_q + 63.999474984100700000000000000000
        return SN3600_hdst
    elif pump == 'QN70':
        QN70_hdst = -0.000000000000000000000092692015*desired_q**6 + 0.000000000000000003989262501640*desired_q**5 - 0.000000000000066398546251239900*desired_q**4 + 0.000000000450657750347824000000*desired_q**3 - 0.000001530354749396110000000000*desired_q**2 - 0.000472159404957040000000000000*desired_q + 46.812981250760500000000000000000
        return QN70_hdst
    elif pump == 'QN120':
        QN120_hdst = 0.000000000000000000000004854677*desired_q**6 + 0.000000000000000000300243096856*desired_q**5 - 0.000000000000016541950707426200*desired_q**4 + 0.000000000228662535744540000000*desired_q**3 - 0.000001208554097794500000000000*desired_q**2 + 0.001399032524332710000000000000*desired_q + 39.465183715140500000000000000000
        return QN120_hdst
    elif pump == 'QM200':
        QM200_hdst = -0.000000000000000000000000586547*desired_q**6 + 0.000000000000000000031705465736*desired_q**5 - 0.000000000000000563101108260672*desired_q**4 - 0.000000000017547770281183500000*desired_q**3 + 0.000000561916392052272000000000*desired_q**2 - 0.005424632929866840000000000000*desired_q + 100.930250926866000000000000000000
        return QM200_hdst
    elif pump == 'QM265':
        QM265_hdst = 0.000000000000000000000000472249*desired_q**6 - 0.000000000000000000019674758089*desired_q**5 + 0.000000000000000056067401267625*desired_q**4 - 0.000000000002159464636267860000*desired_q**3 + 0.000000142240929965327000000000*desired_q**2 - 0.002272609679304340000000000000*desired_q + 108.596020933990000000000000000000
        return QM265_hdst

# Formula for Result

def oilgradient (sg_oil):
    oil_grad = sg_oil*0.433
    return oil_grad

def gasgradient (sg_gas):
    gas_grad = sg_gas*0.433
    return gas_grad

def dynamicliquidlevel (psd, oil_grad, chp, PIP):
    Ldyn = ((psd * oil_grad) + chp - PIP)/(oil_grad)
    return Ldyn

def frictional_headloss (fricloss_hazenwill, tlpsd):
    Hfr = fricloss_hazenwill * (tlpsd/1000)
    return Hfr

def totaldynamichead (Hfr, Ldyn, thp, SG_liquid):
    TDH = (2.31 / SG_liquid) * thp + Ldyn + Hfr
    return TDH

def pumpstages (TDH, hdst): #hpst = head per stages, tergantung pilihan pompanya nanti apa, karena rumus per pompa beda
    Pump_stages = TDH/hdst
    return Pump_stages

def brake_hp (Pump_stages, hpst , liq_grad):
    BHP = Pump_stages * hpst * liq_grad
    return BHP

def brake_hp_with_gas (BHP):
    BHPT = BHP + 5
    return BHPT

def SeparationEfficiency (BHP):
    EffSep = BHP / (BHP + 80)
    return EffSep

def NewIngestedGas (qginsitu, EffNatural):
    qingnew = (qginsitu / 5.61) * (1 - (EffNatural / 100)) * (1 - (80 / 100))
    return qingnew

def totalfluidnew (qingnew, qlpump):
    totalfluid_new = qingnew + qlpump
    return totalfluid_new
