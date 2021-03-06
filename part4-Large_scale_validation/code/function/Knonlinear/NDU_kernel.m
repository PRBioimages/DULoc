
function [X, F, t_ADMM, K] = NDU_kernel(S,R,lambda,mu,rho,nitermax,K)

% 2) initialising
% ----------------
[L, N] = size(S);
P = size(R,2); 
A = [  speye(P); ones(1,P)];   % cst. var. % replace last row by zeros to remove sum-to-one
B = [ -speye(P); zeros(1,P)];  % cst. var. 
C = [0*speye(P,N); ones(1,N)]; % cst. var. % replace last row by zeros to remove sum-to-one 
invAtA = (-1/(P+1))*ones(P,P)+eye(P);

kron_ISA = (1/rho)*kron(eye(N),R*invAtA*R'); % reserves less memory than full() version
Q = eye(L*N) + (1/lambda)*K + kron_ISA;
Q = (Q+Q')/2;

clear kron_ISA; 
[X, ~] = FCLS(S,R); 
Z = X;
Z_old = Z;
V = zeros(P+1,N);
niter = 1;
res = 1;
tol = sqrt(N)*1e-15;

residues = cell(1,2);
for i=1:2
    residues{1,i} = zeros(1,nitermax); % 1 primal residual, 2 dual
end

% ADMM algorithm 
% ---------------
t = clock;
w = zeros(L*N,1); 

while (res > tol) && (niter <= nitermax)
    
    % {X,f} step
    % ----------
    p = vec(S + (1/rho)*R*invAtA*A'*(V+rho*B*Z-rho*C));
    % w = conjgrad(Q,p,w,1e-4,1000) ; % 5
    % [w, flag] = cgs(Q,p,1e-4,1000,[],[],w) ; % 5
    % [w, ~] = pcg(Q,p,tol_pcg,nitermax_pcg,[],[],w) ; % 5
    w = Q\p;
    W = reshape(w,L,N); % E = W ; E is equal to W
    X = (1/rho)*invAtA*(R'*W - A'*V - rho*A'*(B*Z-C));
    
    % Z step - In the supervised consists of projecting on R+
    % --------------------------------------------------------
    Z = max((rho/(rho+mu))*X+(1/(rho+mu))*V(1:end-1,:),0);
    
    % Update Lagrange multipliers
    % ----------------------------
    V = V + rho*(A*X + B*Z - C);
    
    % Stopping criteria
    % -----------------
    res_primal = norm(A*X+B*Z-C,'fro'); % rk
    res_dual = norm(A'*B*(Z_old - Z),'fro'); % sk
    res = res_primal+res_dual;
    Z_old = Z;
    
    % saving residuals
    % -----------------
    residues{1,1}(niter) = res_primal; % primal res. convergence
    residues{1,2}(niter) = res_dual;   % dual res. convergence
    
    % iter count
    % -----------
    niter = niter + 1;
    disp(niter)
    if mod(niter,100000000000)==0
        disp(niter)
    end
end

t_ADMM = etime(clock,t);

F = K*w/lambda; 
F = reshape(F,L,N); % no need for this value at each iteration

