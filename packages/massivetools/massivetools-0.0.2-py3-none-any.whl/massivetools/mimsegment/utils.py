import pickle 
import numpy as np

classes = ('truck' , 'tire')
palette = [[255,255,0] , [0,255,0]]

def pkl2map(pkl_path , dtype = 'label_map'):
    '''
    dtype : [label_map, color_map]
    '''
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    masks = data['masks'].cpu().numpy()
    masks  = masks.transpose(2, 3, 0, 1).squeeze()
    if len(masks.shape) == 2:
        masks = np.expand_dims(masks , axis = -1)
    labels = data['labels']

    
    palette = [[255,255,0] , [0,255,0]]
    labels = np.array(labels)
    st_mask = np.zeros(masks.shape[:2] , dtype = np.int8) 
    for id_ , class_ in enumerate(classes , 1):
        idxs = np.where(labels == class_)[0]
        cat_mask = masks[:,:,idxs]
        if cat_mask.size > 0:
            cat_mask = cat_mask.astype(np.int8)
            cat_mask = np.max(cat_mask , axis = -1) # instance 2 semantic
            cat_mask[np.where(cat_mask != 0)] = id_
            st_mask = np.where(cat_mask != 0 , cat_mask ,st_mask )
        
    if dtype == 'label_map':
        return st_mask

    if dtype == 'color_map':
        rgb_mask = label2palette(st_mask)
        return rgb_mask
    
def label2palette(label_map ):
        # Initialize an empty 3D array for the RGB mask
    rgb_mask = np.zeros((*label_map.shape, 3), dtype=np.uint8)
    # Apply the palette to the label mask
    for idx, color in enumerate(palette , 1):
        rgb_mask[np.where(label_map== idx) ] = color
    return rgb_mask
    
    