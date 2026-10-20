import math

m=75 #mass
g=9.81 #
rho=1.225
CdA=0.35
Crr=0.005
P_crit=380.0
E_ana_max=20000.0
eta=0.5
P_targets=[390, 380, 390, 405, 420, 405, 387, 380, 380, 380
           ]
           

gradients_precent=[2,4,6,8,10,8,6,4,2,0]
thetas=[math.atan(g/100.0)for g in gradients_precent]
distances=[1000.0]*10

def power_equation(v,theta,P):
   F_gravity=m*g*math.sin(theta)
   F_rolling=Crr*m*g*math.cos(theta)
   F_drag=0.5*rho*CdA*v**2
   return (F_gravity+F_rolling)*v+F_drag*v-P
def solve_speed(theta,P):
    low=0.1
    high=100.0
    if power_equation(high,theta,P)<0:
       return high
    for _ in range(100):
        mid=(low+high)/2
        if power_equation(mid,theta,P)<0:
         low=mid
        else:
         high=mid
    return(low+high)/2
    


E_ana=E_ana_max
results=[]
for i in range(10):
    theta=thetas[i]
    ds=distances[i]
    v=solve_speed(theta,P_targets[i])
    dt=ds/v
    if P_targets[i]>P_crit:
        E_ana-=(P_targets[i]-P_crit)*dt
    else:
        E_ana+=eta*(P_crit-P_targets[i])*dt
        E_ana=min(E_ana,E_ana_max)
    results.append({
        "Segment":i+1,
        "Gradient(%)":gradients_precent[i],
        "Speed(m/s)":round(v,2),
        "Time(s)":round(dt,1),
        "E_ana(J)":round(E_ana,1)
        })

print(f"{'Segment':<4}|{'Gradient(%)':<5}|{'Speed(m/s)':<10}|{'Time(s)':<8}|{'E_ana(J)':<10}")
print("-"*50)
for r in results:
    print(f"{r['Segment']:<4}|{r['Gradient(%)']:<5}|{r['Speed(m/s)']:<10}|{r['Time(s)']:<8}|{r['E_ana(J)']:<10}")
total_time=sum(r['Time(s)'] for r in results)
print(f"\nTotal Ascent Time:{total_time}seconds")