function z = zeta(p)
B1=.35;
B2=.24;
for i =-1:1 
    for j = -1:1
    if A(x+i,y+j)==1
        if (i~=0 || j~=0)
   %% zeta = zeta *(1-B*prob(t-1,delta,p,s,x+i,y+j));
    z(1) = z(1) *(1-B1*p(1));
    z(2) = z(2) *(1-B2*p(2));
        end
    end
    end
end