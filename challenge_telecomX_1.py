# Alura Latam G9: Data Science
# Jorge V. Zertuche Rodriguez
# CURSO: Challenge Telecom X: Análisis de Evasión de Clientes, pt.1
# ==========================================================

'''
ESCENARIO
Telecom X es una empresa mexicana con gran presencia en el país. Últimamente, se
ha observado una disminución en la fidelidad de sus clientes (churn).
El objetivo de este análisis es encontrar cualesquiera factores que contribuyen
al churn.
'''

import json
import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format
import matplotlib.pyplot as plt
import numpy as np

colores = {
	'verde_light':"#AFD095",
	'azul_light':"#B4C7DC",
	'azul_dark':"#3498DB",
	'morado_light':"#BF819E",
	'rojo_light':"#EC9BA4",
	'rojo_dark':"#E74C3C",
	'amarillo_light':"#FFFFA6",
	'naranja_light':"#FFB66C",
	'rosa_light':"#FFBCD9",
	'rosa_dark':"#FF2A86",
	'gris_light':"#B2B2B2"
}

with open('data/TelecomX_Data.json','r') as f:
	clientes = pd.json_normalize(json.load(f))
clientes.columns = [col.replace(".","_").lower() for col in clientes.columns]

# Primera visualización de los datos
print()
print("	 Base de datos inicial")
print("="*51)
clientes.info()
print()

# Decidir si eliminar churn desconocido
churn_yesno = (clientes["churn"]!='').sum()
churn_unkown = (clientes["churn"]=='').sum()
ch_yn_male = ((clientes["churn"]!='')&(clientes["customer_gender"]=='Male')).sum()/churn_yesno*100
ch_yn_female = ((clientes["churn"]!='')&(clientes["customer_gender"]=='Female')).sum()/churn_yesno*100
ch_uk_male = ((clientes["churn"]=='')&(clientes["customer_gender"]=='Male')).sum()/churn_unkown*100
ch_uk_female = ((clientes["churn"]=='')&(clientes["customer_gender"]=='Female')).sum()/churn_unkown*100
ch_yn_senior = ((clientes["churn"]!='')&(clientes["customer_seniorcitizen"]==1)).sum()/churn_yesno*100
ch_uk_senior = ((clientes["churn"]=='')&(clientes["customer_seniorcitizen"]==1)).sum()/churn_unkown*100
ch_yn_partner = ((clientes["churn"]!='')&(clientes["customer_partner"]=='Yes')).sum()/churn_yesno*100
ch_uk_partner = ((clientes["churn"]=='')&(clientes["customer_partner"]=='Yes')).sum()/churn_unkown*100
ch_yn_dependents = ((clientes["churn"]!='')&(clientes["customer_dependents"]=='Yes')).sum()/churn_yesno*100
ch_uk_dependents = ((clientes["churn"]=='')&(clientes["customer_dependents"]=='Yes')).sum()/churn_unkown*100
ch_yn_tenure = clientes[clientes["churn"]!='']["customer_tenure"].mean()
ch_uk_tenure = clientes[clientes["churn"]=='']["customer_tenure"].mean()
ch_yn_monthly_charge = clientes[clientes["churn"]!='']["account_charges_monthly"].mean()
ch_uk_monthly_charge = clientes[clientes["churn"]=='']["account_charges_monthly"].mean()
print("	 Comparativa entre poblaciones según churn")
print("="*51)
print("\t\t\tSí/No\t\tDesconocido")
print(f"Total\t\t\t{churn_yesno}\t\t{churn_unkown}")
print(f"Masculino (%)\t\t{ch_yn_male:.1f}\t\t{ch_uk_male:.1f}")
print(f"Femenino(%)\t\t{ch_yn_female:.1f}\t\t{ch_uk_female:.1f}")
print(f"Edad >65 (%)\t\t{ch_yn_senior:.1f}\t\t{ch_uk_senior:.1f}")
print(f"Tiene pareja (%)\t{ch_yn_partner:.1f}\t\t{ch_uk_partner:.1f}")
print(f"Tiene dependientes (%)\t{ch_yn_dependents:.1f}\t\t{ch_uk_dependents:.1f}")
print(f"Tenencia (meses)\t{ch_yn_tenure:.1f}\t\t{ch_uk_tenure:.1f}")
print(f"Cargos mensuales ($)\t{ch_yn_monthly_charge:.2f}\t\t{ch_uk_monthly_charge:.2f}")
print()

# Limpieza de los datos
'''
customerid:					[multiple]
churn:						['No' 'Yes' '']
customer_gender:			['Female' 'Male']
customer_seniorcitizen:		[0 1]
customer_partner:			['Yes' 'No']
customer_dependents:		['Yes' 'No']
customer_tenure:			[multiple]
phone_phoneservice:			['Yes' 'No']
phone_multiplelines:		['No' 'Yes' 'No phone service']
internet_internetservice:	['DSL' 'Fiber optic' 'No']
internet_onlinesecurity:	['No' 'Yes' 'No internet service']
internet_onlinebackup:		['Yes' 'No' 'No internet service']
internet_deviceprotection:	['No' 'Yes' 'No internet service']
internet_techsupport:		['Yes' 'No' 'No internet service']
internet_streamingtv:		['Yes' 'No' 'No internet service']
internet_streamingmovies:	['No' 'Yes' 'No internet service']
account_contract:			['One year' 'Month-to-month' 'Two year']
account_paperlessbilling:	['Yes' 'No']
account_paymentmethod:		['Mailed check' 'Electronic check' 'Credit card (automatic)' 'Bank transfer (automatic)']
account_charges_monthly:	[multiple]
account_charges_total:		[multiple]
'''
clientes = clientes.drop("customerid",axis=1)
clientes = clientes[clientes["churn"]!='']
clientes["customer_seniorcitizen"] = clientes["customer_seniorcitizen"].astype(int)
clientes["customer_gender"] = clientes["customer_gender"].map({'Male':1,'Female':0}).astype(int)
for col in ["churn","customer_partner","customer_dependents","phone_phoneservice","account_paperlessbilling"]:
	clientes[col] = clientes[col].map({'Yes':1,'No':0}).astype(int)
clientes["phone_multiplelines"] = clientes["phone_multiplelines"].map({'Yes':1,'No':0,'No phone service':0}).astype(int)
for col in ["onlinesecurity","onlinebackup","deviceprotection","techsupport","streamingtv","streamingmovies"]:
	clientes[f"internet_{col}"] = clientes[f"internet_{col}"].map({'Yes':1, 'No':0, 'No internet service':0}).astype(int)
tenure_zero = list(clientes[clientes["customer_tenure"]==0].index)
year_charge_empty = list(clientes[clientes["account_charges_total"]==' '].index)
month_charge_empty = list(clientes[clientes["account_charges_total"]==' '].index)
if tenure_zero == year_charge_empty:
	for col in ["monthly","total"]:
		clientes[f"account_charges_{col}"] = (clientes[f"account_charges_{col}"].replace(' ',0)).astype(float)
categoricals = {
	'DSL':"dsl",
	'Fiber optic':"fiberoptic",
	'No':"noservice",
	'One year':"1yr",
	'Two year':"2yr",
	'Month-to-month':"monthly",
	'Mailed check':"mailcheck",
	'Electronic check':"echeck",
	'Credit card (automatic)':"credit",
	'Bank transfer (automatic)':"transfer"
}
for col in ["internet_internetservice","account_contract","account_paymentmethod"]:
	clientes[col] = clientes[col].map(categoricals)
for col,pref in [("internet_internetservice","internet"),("account_contract","contract"),("account_paymentmethod","payment")]:
	dummies = pd.get_dummies(clientes[col],prefix=pref).astype(int)
	clientes = pd.concat([clientes,dummies],axis=1)
	clientes = clientes.drop(col,axis=1)
print("	 Limpieza de la base de datos")
print("="*51)
print(f"Clientes con tenencia cero:\t\t{len(tenure_zero)}")
print(f"Clientes con cargo mensual nulo:\t{len(month_charge_empty)}")
print(f"Clientes con cargos totales nulos:\t{len(year_charge_empty)}")
if tenure_zero == year_charge_empty == month_charge_empty:
	print("Se trata de los mismos clientes en estos casos.")
else:
	print("No se trata de los mismos clientes.")
print()

# Base de datos limpia
'''
churn:						[0 1]
customer_gender:			[0 1]
customer_seniorcitizen:		[0 1]
customer_partner:			[1 0]
customer_dependents:		[1 0]
customer_tenure:			[multiple]
phone_phoneservice:			[1 0]
phone_multiplelines:		[0 1]
internet_onlinesecurity:	[0 1]
internet_onlinebackup:		[1 0]
internet_deviceprotection:	[0 1]
internet_techsupport:		[1 0]
internet_streamingtv:		[1 0]
internet_streamingmovies:	[0 1]
account_paperlessbilling:	[1 0]
account_charges_monthly:	[multiple]
account_charges_total:		[multiple]
internet_dsl:				[1 0]
internet_fiberoptic:		[0 1]
internet_noservice:			[0 1]
contract_1yr:				[1 0]
contract_2yr:				[0 1]
contract_monthly:			[0 1]
payment_credit:				[0 1]
payment_echeck:				[0 1]
payment_mailcheck:			[1 0]
payment_transfer:			[0 1]
'''
print("	 Base de datos limpia")
print("="*51)
clientes.info()
print()

# Guardando la base de datos limpia
clientes.to_csv('data_TelecomX_clean.csv',index=False)

# Verificando errores
phone_errors = list(clientes[(clientes["phone_phoneservice"]==0)&(clientes["phone_multiplelines"]==1)].index)
internet_errors = list(clientes[(clientes["internet_noservice"]==1)&((clientes["internet_dsl"]==1)|(clientes["internet_fiberoptic"]==1))].index)
contract_errors = list(clientes[(clientes["contract_monthly"]==1)&((clientes["contract_1yr"]==1)|(clientes["contract_2yr"]==1))].index)
payment_multiple = list(clientes[(clientes["payment_credit"]+clientes["payment_echeck"]+clientes["payment_mailcheck"]+clientes["payment_transfer"])>1].index)
payment_none = list(clientes[(clientes["payment_credit"]+clientes["payment_echeck"]+clientes["payment_mailcheck"]+clientes["payment_transfer"])==0].index)
print("	 Errores en los registros")
print("="*51)
print(f"Clientes sin teléfono con múltiples líneas:\t{len(phone_errors)}")
print(f"Clientes sin internet pero con DSL/fibra:\t{len(internet_errors)}")
print(f"Clientes con contratos múltiples:\t\t{len(contract_errors)}")
print(f"Clientes con más de una forma de pago:\t\t{len(payment_multiple)}")
print(f"Clientes sin forma de pago:\t\t\t{len(payment_none)}")
print()

# Clientes con sobrecargos o subcargos
clientes["account_overpay"] = clientes["account_charges_total"]-clientes["customer_tenure"]*clientes["account_charges_monthly"]
print("	 Sobrecargos en el pago de los clientes")
print("="*51)
print(clientes["account_overpay"].describe())
print()

# Porcentaje de churn
clientes_total = len(clientes)
churn_yes = (clientes["churn"]==1).sum()
churn_no = (clientes["churn"]==0).sum()
print("="*51)
print(f"   CLIENTES QUE ABANDONARON LA COMPAÑÍA:  {churn_yes/clientes_total*100:.1f} %")
print("="*51)
print()
# plt.figure(figsize=(12,8))
# plt.pie([churn_yes,churn_no],labels=["Sí","No"],colors=[colores["rojo_light"],colores["gris_light"]],textprops={'fontsize':14},autopct="%1.1f%%")
# plt.suptitle("Porcentaje de Clientes que Abandonaron Telecom X",fontsize=16)
# plt.tight_layout()
# plt.savefig('images/1_churn_pct_total.png',dpi=300)
# plt.show()

# Características de los clientes
males_cats = females_cats = ["<65 años","65+ años"]
males = [((clientes["customer_gender"]==1)&(clientes["customer_seniorcitizen"]==0)).sum(),
         ((clientes["customer_gender"]==1)&(clientes["customer_seniorcitizen"]==1)).sum()]
females = [((clientes["customer_gender"]==0)&(clientes["customer_seniorcitizen"]==0)).sum(),
           ((clientes["customer_gender"]==0)&(clientes["customer_seniorcitizen"]==1)).sum()]
# plt.figure(figsize=(12,8))
# plt.pie([sum(males),sum(females)],labels=["Hombres","Mujeres"],colors=[colores["azul_light"],colores["rosa_light"]],textprops={'fontsize':14},autopct="%1.1f%%",startangle=45)
# plt.suptitle("Sexo de los Clientes",fontsize=16)
# plt.tight_layout()
# plt.savefig('images/2_sexo_pct_total.png',dpi=300)
# plt.show()
# fig,(ax1,ax2) = plt.subplots(1,2,figsize=(12,8))
# ax1.bar(males_cats,[males[0],males[1]],color=[colores["azul_light"],colores["azul_dark"]],zorder=3)
# ax1.tick_params(axis='x',labelsize=12)
# ax1.set_xlabel("Hombres",fontsize=14)
# ax1.set_ylabel("Clientes",fontsize=14)
# ax1.grid(axis='y',alpha=0.30,zorder=0)
# ax1.set_ylim(0,3000)
# ax2.bar(females_cats,[females[0],females[1]],color=[colores["rosa_light"],colores["rosa_dark"]],zorder=3)
# ax2.tick_params(axis='x',labelsize=12)
# ax2.set_xlabel("Mujeres",fontsize=14)
# ax2.grid(axis='y',alpha=0.30,zorder=0)
# ax2.set_ylim(0,3000)
# plt.suptitle("Edad de los Clientes",fontsize=16)
# plt.tight_layout()
# plt.savefig('images/3_sexo_edades.png',dpi=300)
# plt.show()
churn_males = [((clientes["customer_gender"]==1)&(clientes["customer_seniorcitizen"]==0)&(clientes["churn"]==1)).sum(),
		       ((clientes["customer_gender"]==1)&(clientes["customer_seniorcitizen"]==1)&(clientes["churn"]==1)).sum()]
churn_females = [((clientes["customer_gender"]==0)&(clientes["customer_seniorcitizen"]==0)&(clientes["churn"]==1)).sum(),
                 ((clientes["customer_gender"]==0)&(clientes["customer_seniorcitizen"]==1)&(clientes["churn"]==1)).sum()]
# fig,(ax1,ax2) = plt.subplots(1,2,figsize=(12,8))
# ax1.pie([churn_males[0],males[0]-churn_males[0]],labels=["Sí","No"],colors=[colores["rojo_light"],colores["azul_light"]],textprops={'fontsize':12},autopct="%1.1f%%")
# ax1.set_title("Hombres",fontsize=14)
# ax2.pie([churn_females[0],females[0]-churn_females[0]],labels=["Sí","No"],colors=[colores["rojo_light"],colores["rosa_light"]],textprops={'fontsize':12},autopct="%1.1f%%")
# ax2.set_title("Mujeres",fontsize=14)
# plt.suptitle("Clientes de <65 años que Abandonaron Telecom X",fontsize=16)
# plt.tight_layout()
# plt.savefig('images/4_churn_pct_young.png',dpi=300)
# plt.show()
# fig,(ax1,ax2) = plt.subplots(1,2,figsize=(12,8))
# ax1.pie([churn_males[1],males[1]-churn_males[1]],labels=["Sí","No"],colors=[colores["rojo_light"],colores["azul_dark"]],textprops={'fontsize':12},autopct="%1.1f%%")
# ax1.set_title("Hombres",fontsize=14)
# ax2.pie([churn_females[1],females[1]-churn_females[1]],labels=["Sí","No"],colors=[colores["rojo_light"],colores["rosa_dark"]],textprops={'fontsize':12},autopct="%1.1f%%")
# ax2.set_title("Mujeres",fontsize=14)
# plt.suptitle("Clientes de 65+ años que Abandonaron Telecom X",fontsize=16)
# plt.tight_layout()
# plt.savefig('images/5_churn_pct_old.png',dpi=300)
# plt.show()
partner_males = [((clientes["customer_gender"]==1)&(clientes["customer_seniorcitizen"]==0)&(clientes["customer_partner"]==1)).sum(),
		         ((clientes["customer_gender"]==1)&(clientes["customer_seniorcitizen"]==1)&(clientes["customer_partner"]==1)).sum()]
partner_females = [((clientes["customer_gender"]==0)&(clientes["customer_seniorcitizen"]==0)&(clientes["customer_partner"]==1)).sum(),
		           ((clientes["customer_gender"]==0)&(clientes["customer_seniorcitizen"]==1)&(clientes["customer_partner"]==1)).sum()]
deps_males = [((clientes["customer_gender"]==1)&(clientes["customer_seniorcitizen"]==0)&(clientes["customer_dependents"]==1)).sum(),
		      ((clientes["customer_gender"]==1)&(clientes["customer_seniorcitizen"]==1)&(clientes["customer_dependents"]==1)).sum()]
deps_females = [((clientes["customer_gender"]==0)&(clientes["customer_seniorcitizen"]==0)&(clientes["customer_dependents"]==1)).sum(),
		        ((clientes["customer_gender"]==0)&(clientes["customer_seniorcitizen"]==1)&(clientes["customer_dependents"]==1)).sum()]
print("	 Demografía de los clientes")
print("="*51)
print("\t\tHombres\t\tMujeres")
print("-"*51)
print("\t"*3+"Totales")
print(f"\t\t{sum(males)} ({sum(males)/clientes_total:.1%})\t{sum(females)} ({sum(females)/clientes_total:.1%})")
print("\t"*3+"Edad")
print(f"<65 años\t{males[0]} ({males[0]/sum(males):.1%})\t{females[0]} ({females[0]/sum(females):.1%})")
print(f"65+ años\t{males[1]} ({males[1]/sum(males):.1%})\t{females[1]} ({females[1]/sum(females):.1%})")
print("\t"*3+"Churn")
print(f"<65 años\t{churn_males[0]} ({churn_males[0]/males[0]:.1%})\t{churn_females[0]} ({churn_females[0]/females[0]:.1%})")
print(f"65+ años\t{churn_males[1]} ({churn_males[1]/males[1]:.1%})\t{churn_females[1]} ({churn_females[1]/females[1]:.1%})")
print("\t"*3+"Tienen pareja")
print(f"<65 años\t{partner_males[0]} ({partner_males[0]/males[0]:.1%})\t{partner_females[0]} ({partner_females[0]/females[0]:.1%})")
print(f"65+ años\t{partner_males[1]} ({partner_males[1]/males[1]:.1%})\t{partner_females[1]} ({partner_females[1]/females[1]:.1%})")
print("\t"*3+"Tienen dependientes")
print(f"<65 años\t{deps_males[0]} ({deps_males[0]/males[0]:.1%})\t{deps_females[0]} ({deps_females[0]/females[0]:.1%})")
print(f"65+ años\t{deps_males[1]} ({deps_males[1]/males[1]:.1%})\t{deps_females[1]} ({deps_females[1]/females[1]:.1%})")
print()

# Base de datos de churn
churns = clientes[clientes["churn"]==1].copy()
print("	 Base de datos de churn")
print("="*51)
churns.info()
print()

# Características del churn
churns_only_phone = ((churns["phone_phoneservice"]==1)&(churns["internet_noservice"]==1)).sum()
churns_only_internet = ((churns["phone_phoneservice"]==0)&(churns["internet_noservice"]==0)).sum()
churns_both_phint = ((churns["phone_phoneservice"]==1)&(churns["internet_noservice"]==0)).sum()
churns_nothing = ((churns["phone_phoneservice"]==0)&(churns["internet_noservice"]==1)).sum()
churns_multilines = (churns["phone_multiplelines"]==1).sum()
churns_internet_type = [(churns["internet_dsl"]==1).sum(),
                        (churns["internet_fiberoptic"]==1).sum()]
churns_multiinter = ((churns["internet_onlinebackup"]+
                      churns["internet_deviceprotection"]+
                      churns["internet_techsupport"]+
                      churns["internet_streamingtv"]+
                      churns["internet_streamingmovies"])>1).sum()
churns_internet_services = [churns["internet_onlinebackup"].sum(),
                            churns["internet_deviceprotection"].sum(),
                            churns["internet_techsupport"].sum(),
                           (churns["internet_streamingtv"]+churns["internet_streamingmovies"]).sum()]
churns_billing = churns["account_paperlessbilling"].sum()
churns_payment = [churns["payment_credit"].sum(),
                  churns["payment_echeck"].sum(),
                  churns["payment_mailcheck"].sum(),
                  churns["payment_transfer"].sum()]
churns_contract = [churns["contract_1yr"].sum(),
                   churns["contract_2yr"].sum(),
                   churns["contract_monthly"].sum()]
print("	 Características de los clientes churn")
print("="*51)
print(f"Sólo servicio telefónico:\t\t{churns_only_phone} ({churns_only_phone/len(churns):.1%})")
print(f"Sólo servicio de internet:\t\t{churns_only_internet} ({churns_only_internet/len(churns):.1%})")
print(f"Servicio de teléfono+internet:\t\t{churns_both_phint} ({churns_both_phint/len(churns):.1%})")
print(f"Sin servicio:\t\t\t\t{churns_nothing}")
print(f"Múltiples líneas telefónicas:\t\t{churns_multilines} ({churns_multilines/len(churns):.1%})")
print(f"Tipo de servicio de internet:")
for i,col in enumerate(["internet_dsl","internet_fiberoptic"]):
	print(f"\t{col[9:]:<32}{churns_internet_type[i]} ({churns_internet_type[i]/sum(churns_internet_type):.1%})")
print(f"Múltiples servicios de internet:")
for i,col in enumerate(["internet_onlinebackup","internet_deviceprotection","internet_techsupport","internet_streaming"]):
	print(f"\t{col[9:]:<32}{churns_internet_services[i]} ({churns_internet_services[i]/sum(churns_internet_services):.1%})")
print(f"Recibo paperless:\t\t\t{churns_billing} ({churns_billing/len(churns):.1%})")
print(f"Forma de pago:")
for i,col in enumerate(["payment_credit","payment_echeck","payment_mailcheck","payment_transfer"]):
	print(f"\t{col[8:]:<32}{churns_payment[i]} ({churns_payment[i]/sum(churns_payment):.1%})")
print(f"Tipo de contrato:")
for i,col in enumerate(["contract_1yr","contract_2yr","contract_monthly"]):
	print(f"\t{col[9:]:<32}{churns_contract[i]} ({churns_contract[i]/sum(churns_contract):.1%})")
print(f"Sobrecargo y subcargo:")
print(churns["account_overpay"].describe())
print()

# Clientes fieles en riesgo
loyals = clientes[clientes["churn"]==0].copy()
loyals["risk"] = (loyals["customer_seniorcitizen"]==1).astype(int)+((loyals["phone_phoneservice"]==1)&(loyals["internet_noservice"]==0)).astype(int)+(loyals["phone_multiplelines"]==1).astype(int)+(loyals["internet_fiberoptic"]==1).astype(int)+((loyals["internet_streamingtv"]==1)|(loyals["internet_streamingmovies"]==1)).astype(int)+(loyals["account_paperlessbilling"]==1).astype(int)+(loyals["payment_echeck"]==1).astype(int)+(loyals["contract_monthly"]==1).astype(int)
churns["risk"] = (churns["customer_seniorcitizen"]==1).astype(int)+((churns["phone_phoneservice"]==1)&(churns["internet_noservice"]==0)).astype(int)+(churns["phone_multiplelines"]==1).astype(int)+(churns["internet_fiberoptic"]==1).astype(int)+((churns["internet_streamingtv"]==1)|(churns["internet_streamingmovies"]==1)).astype(int)+(churns["account_paperlessbilling"]==1).astype(int)+(churns["payment_echeck"]==1).astype(int)+(churns["contract_monthly"]==1).astype(int)
risk_grades = churn_grades = ["0-1 (bajo)","2-3 (medio)","4+ (alto)"]
risk_vals = [(loyals["risk"]<=1).sum(),
            ((loyals["risk"]>=2)&(loyals["risk"]<=3)).sum(),
             (loyals["risk"]>=4).sum()]
churn_vals = [(churns["risk"]<=1).sum(),
             ((churns["risk"]>=2)&(churns["risk"]<=3)).sum(),
              (churns["risk"]>=4).sum()]
print("	 Factores de riesgo en clientes fieles")
print("="*51)
print("* Edad >65 años")
print("* Servicio de teléfono+internet")
print("* Múltiples líneas telefónicas")
print("* Internet de fibra óptica")
print("* Streaming (cualquier servicio)")
print("* Recibo paperless")
print("* Pago por cheque electrónico")
print("* Contratación mensual")
print()
print("	 Clientes fieles en riesgo de abandono")
print("="*51)
print("\tFactores de riesgo\tClientes")
for i in range(3):
	print(f"\t{risk_grades[i]}\t\t{risk_vals[i]}")
print()
pie_grades = ["Bajo","Medio","Alto"]
# fig,(ax1,ax2) = plt.subplots(1,2,figsize=(12,8))
# ax1.pie(risk_vals,labels=pie_grades,colors=[colores["verde_light"],colores["amarillo_light"],colores["rojo_light"]],textprops={'fontsize':12},autopct="%1.1f%%")
# ax1.set_title("Clientes Fieles",fontsize=14)
# ax2.pie(churn_vals,labels=pie_grades,colors=[colores["verde_light"],colores["amarillo_light"],colores["rojo_light"]],textprops={'fontsize':12},autopct="%1.1f%%")
# ax2.set_title("Clientes que Abandonaron",fontsize=14)
# plt.suptitle("Grados de Riesgo de Abandono",fontsize=16)
# plt.tight_layout()
# plt.savefig('images/6_loyals_risk_factors.png',dpi=300)
# plt.show()
