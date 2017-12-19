# extend single array (N1*4 + 8, N1 + N2 + 4)
def exch_array(arr0):
    
    dims = arr0.shape
    tilesize1 = dims[0]/4                # 90
    tilesize2 = dims[1]-dims[0]/4        # 270
    outsize1 = 4*(tilesize1+2)           # 368
    outsize2 = tilesize1 + tilesize2 + 4 # 364
    
    arr = np.nan * np.zeros([outsize1,outsize2])

    # 1st
    arr[0,1:tilesize2+1] = arr0[-1,:tilesize2]
    arr[1:tilesize1+1,1:tilesize2+2] = arr0[0:tilesize1,0:tilesize2+1]
    arr[tilesize1+1,1:tilesize2+1] = arr0[tilesize1,:tilesize2]
    # 1st right (polus)
    arr[1:tilesize1+1,tilesize2+3] = arr0[0:tilesize1,tilesize2]
    arr[1:tilesize1+1,tilesize2+2] = arr0[0:tilesize1,tilesize2-1]
    arr[1:tilesize1+1,tilesize2+3:tilesize1+tilesize2+3] = arr0[0:tilesize1,tilesize2:]
    # rigth vertical line
    arr[1:tilesize1+1,tilesize1+tilesize2+3:] = np.flipud(arr0[2*tilesize1:3*tilesize1,tilesize2-1]).reshape([tilesize1,1])
    # top horizontal line
    arr[tilesize1+1,tilesize2+3:tilesize1+tilesize2+3] = np.transpose(arr0[tilesize1:2*tilesize1,tilesize2-1])
    # bottom horizontal line
    arr[0,tilesize2+3:tilesize1+tilesize2+3] = np.transpose(np.flipud(arr0[3*tilesize1:4*tilesize1,tilesize2-1]))

    # 2nd
    arr[tilesize1+2,1:tilesize2+1] = arr0[tilesize1-1,:tilesize2]
    arr[tilesize1+3:2*tilesize1+3,1:tilesize2+1] = arr0[tilesize1:2*tilesize1,0:tilesize2]
    arr[2*tilesize1+3,1:tilesize2+1] = arr0[2*tilesize1,0:tilesize2]
    # right vertical line
    arr[tilesize1+3:2*tilesize1+3,tilesize2+1] = arr0[tilesize1-1,tilesize2:tilesize1+tilesize2]

    # 3rd
    arr[2*tilesize1+4,1:tilesize2+1] = arr0[2*tilesize1-1,0:tilesize2]
    arr[2*tilesize1+5:3*tilesize1+5,1:tilesize2+1] = arr0[2*tilesize1:3*tilesize1,0:tilesize2]
    arr[3*tilesize1+5,1:tilesize2+1] = arr0[3*tilesize1,0:tilesize2]
    # right vertical line
    arr[2*tilesize1+5:3*tilesize1+5,tilesize2+1] = np.flipud(arr0[0:tilesize1,tilesize1+tilesize2-1])

    # 4th
    arr[3*tilesize1+6,1:tilesize2+1] = arr0[3*tilesize1-1,0:tilesize2]
    arr[3*tilesize1+7:4*tilesize1+7,1:tilesize2+1] = arr0[3*tilesize1:4*tilesize1,0:tilesize2]
    arr[4*tilesize1+7,1:tilesize2+1] = arr0[0,0:tilesize2]
    # right vertical line
    arr[3*tilesize1+7:4*tilesize1+7,tilesize2+1] = np.flipud(arr0[0,tilesize2:tilesize1+tilesize2])

    return arr
   
# split extended single array (N1*4 + 8, N1 + N2 + 4) to extended gcmfaces (N1,N2),(N1,N1),(N2,N1)
def exch_array2exch_faces(arr):
    
    dims = arr.shape
    tilesize1 = dims[0]/4 - 2                # 90
    tilesize2 = dims[1] - (tilesize1+2) - 2  # 270
    
    f1 = arr[0:tilesize1+2,0:tilesize2+2]
    f2 = arr[tilesize1+2:2*tilesize1+4,0:tilesize2+2]
    f3 = np.rot90(arr[0:tilesize1+2,tilesize2+2:],-1)
    f4 = np.rot90(arr[2*tilesize1+4:3*tilesize1+6,0:tilesize2+2])
    f5 = np.rot90(arr[3*tilesize1+6:4*tilesize1+8,0:tilesize2+2])

    return [f1,f2,f3,f4,f5]

# wrapper function for Matlab code
def exch_T_N(arr0):
    return exch_array2exch_faces(exch_array(arr0))


def exch_UV(fldU,fldV):
    (FLDUtmp_f1,FLDUtmp_f2,FLDUtmp_f3,FLDUtmp_f4,FLDUtmp_f5) = exch_T_N(fldU)
    (FLDVtmp_f1,FLDVtmp_f2,FLDVtmp_f3,FLDVtmp_f4,FLDVtmp_f5) = exch_T_N(fldV)
    
    FLDU_f1 = FLDUtmp_f1[1:,1:-1]
    FLDV_f1 = FLDVtmp_f1[1:-1,1:]
    FLDV_f1[:,-1] = FLDUtmp_f1[1:-1,-1]

    FLDU_f2 = FLDUtmp_f2[1:,1:-1]  
    FLDU_f2[-1,:]=FLDVtmp_f2[-1,1:-1]
    FLDV_f2 = FLDVtmp_f2[1:-1,1:]
    
    FLDU_f3 = FLDUtmp_f3[1:,1:-1]
    FLDV_f3 = FLDVtmp_f3[1:-1,1:]
    FLDV_f3[:,-1] = FLDUtmp_f3[1:-1,-1]
    
    FLDU_f4 = FLDUtmp_f4[1:,1:-1]
    FLDV_f4 = FLDVtmp_f4[1:-1,1:]
    
    FLDU_f5 = FLDUtmp_f5[1:,1:-1]
    FLDV_f5 = FLDVtmp_f5[1:-1,1:]
    FLDV_f5[:,-1] = FLDUtmp_f5[1:-1,-1]
    
    return ((FLDU_f1,FLDU_f2,FLDU_f3,FLDU_f4,FLDU_f5), (FLDV_f1,FLDV_f2,FLDV_f3,FLDV_f4,FLDV_f5))

def calc_UV_conv(fldU,fldV):
    
    (FLDU,FLDV) = exch_UV(fldU,fldV)
    for face in range(0,5):
        FLDU[face][np.isnan(FLDU[face])] = 0
        FLDV[face][np.isnan(FLDV[face])] = 0

    fldDIV = []
    for face in range(0,5):
        fldDIV_face = FLDU[face][:-1,:] - FLDU[face][1:,:] + FLDV[face][:,:-1] - FLDV[face][:,1:]
        fldDIV.append(fldDIV_face)
    
    return fldDIV
    
  
