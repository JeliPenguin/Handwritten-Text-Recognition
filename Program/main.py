from Session import Session


exiting = False
while not exiting: #Objective 1.f
    main = Session() #Initiate new session
    main.update_time()
    main.startup_window()
    if not main.operation_type == '':
        folder_structure = main.create_folder_structure()
        main.preprocess_image(main.image_path,folder_structure)
        main.CNN_prediction(folder_structure)
    else:
        exiting = True
