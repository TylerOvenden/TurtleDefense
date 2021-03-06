%% SIR_Model
%%Adapted from Kurt Owen yt vid
%%State var of  SIR
%%Pararmeters
I0 = .01; %Initial proportion infected
a = 1.1; % I coefficient in t -1
b = 0.05; % R coefficient

tmax = 30; %number of iterations
dt = 1; % size of time step in t
Imax = 1.1; % Max number infected for graph 
%%Initiliaze vectors
plotchoice = 3; % 1 =S, 2 = I , 3 = R, 4 = ALL
t = 0:dt:tmax;% time vector
Nt = length(t);%# of steps
I  = zeros(1,Nt);%infected vectors
S = zeros(1,Nt);%susceptible vectors
R = zeros(1,Nt);
I(1)=I0;
%%Calculations
 for it = 1:Nt-1
     S(it) = 1 - I(it)-R(it);
     dI = a * I(it)*S(it)-b*I(it);%rate of change
     I(it+1)= I(it)+dI*dt;
     dR = b*I(it);
     R(it+1) = R(it) + dR*dt;
 end
 S(Nt)= 1 -I(Nt)-R(Nt);
%%plots
 
        plot(t,S,'-b','LineWidth',2)
        hold on
        plot(t,I,'-r','LineWidth',2)
        plot(t,R,'-g','LineWidth',2)
        legend('Susceptible','Infected','Recovered')
        hold off
        axis([0 tmax 0 Imax])
        grid on
        grid minor
        xlabel('t')
        ylabel('Proportion ')
        title('Susceptible')

