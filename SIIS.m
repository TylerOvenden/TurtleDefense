%clc
rng('shuffle');%%seed rnd 
N = 10;
Tm = 1000;
beta1 = .0005;
beta2 = .0005;
delta1 =.004;
delta2 = .004;
adj1 = randi([0,1], N);
B=adj1'+adj1;
B(1:N+1:end)=diag(adj1);
adj1 = mod(B,2);
adj2 = randi([0,1], N);
B=adj2'+adj2;
B(1:N+1:end)=diag(adj2);
adj2 = mod(B,2);
node = randi([0,2],1,N);
infected_meme1 = zeros(Tm);
infected_meme2 = zeros(Tm);
S1 = (1- delta1)*eye(N) + beta1*adj1;
S2 = (1- delta2)*eye(N) + beta1*adj2;
Eig1 = eigs(S1,2)
Eig2 = eigs(S2,2)
for t = 1:Tm
  for nd = 1:N
       C1 = 0;
       C2 = 0;
      
    if node(nd) == 0
      for nb = 1:N
          if adj1(nd,nb) == 1
            if node(nb) == 1 && rand(1)<beta1 
                C1=C1+1;
            end
             if node(nb) == 2 && rand(1)<beta2 
                C2=C2+1;
            end
          end
      end
       if   C1>C2
           node(nd) = 1;
       end
       if C2>C1 
           node(nd) = 2;
       end
      else
             if node(nd) == 1 && rand(1)<delta1 
               node(nd) = 0;
             elseif node(nd) == 2 && rand(1)<delta1
                node(nd) = 0;
            end
    end
   end
   infected_meme1(t) = sum(node(:) == 1);
   infected_meme2(t) = sum(node(:) == 2);
end
x = linspace(1,Tm,Tm);
%disp(node);
%figure
plot(x,infected_meme1,'red',x,infected_meme2,'blue')
clearvars()
