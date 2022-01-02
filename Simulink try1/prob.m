function p = prob(x,y,zeta,tau,past,prevsus)
%%need to test
%%need to build a way to implement in large scale using adjacency matrix
%%check what outputting
%%
    past = input(1);
    prevsus = input(2);
    
    delta1=.50;
    delta2=.50;
    x=x;
    y=y;

    p(1)=(1-delta1)*past(1) + tau(zeta(past))*sus(input);
    p(1)=(1-delta2)*past(1) + tau(zeta(past))*sus(input);


end