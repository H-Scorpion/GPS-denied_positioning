# Task 
1. Receive reference gps data from anchor (Can be done by key in anchor GPS coordinate as well)
2. Receive relative position from UWB
3. Calculate absolute position
4. send absolute gps position to the FC

# Workflow
1. check "connection_data.json" to make sure all connection COM ports are correct.
2. run "anchor_tag_dis.py" the make sure we're able to read UWB distance data.
# Files & Functions
## anchor_tag_dis.py
Read data from UWB anchor
To check whether we read the 
UWB distance data properly.
