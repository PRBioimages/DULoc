function x = gnf_lsqlin(base,mix)
% Use constrained optimization to solve the linear mixture
%
% Author: T. Peng
% Created: 10-Sep-2009
% Last Update: 23-Dec-2009
%
% Copyright (C) 2008-2010 Murphy Lab, Carnegie Mellon University
%
% This program is free software; you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published
% by the Free Software Foundation; either version 2 of the License,
% or (at your option) any later version.
%
% This program is distributed in the hope that it will be useful, but
% WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
% General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program; if not, write to the Free Software
% Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
% 02110-1301, USA.
%
% For additional information visit http://murphylab.web.cmu.edu or
% send email to murphy@cmu.edu


N = size(base,2);

opts = optimset('LargeScale','off');
x = lsqlin(base,mix,[],[],ones(1,N),1,zeros(N,1),[],ones(N,1)/N,opts);