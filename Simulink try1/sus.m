function s = sus(input)
p=input(1);
prev_sus = input(2);
delta1=.50;
delta2=.50;
t1= t(1);
t2= t(2);

s= (1-t1-t2)*prev_sus + delta1*p(1)+delta2*p(2);
    
end