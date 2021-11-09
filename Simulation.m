N=100;
%Create Array of nodes
nodes = ObjectArray(2*N);
%First network occupies the first N nodes
for k = 1:N
    nodes(k) = node(k);
    %nodes(k).nodeNum = k;
end
%Second network occupies the second N nodes
for k = N+1:2*N
    nodes(k) = node(k-N);
    %nodes(k).nodeNum = k-N;
end
%create adjaceny matrixes of both networks
A1 = randi([0,1],[N,N]);
A2 = randi([0,1],[N,N]);