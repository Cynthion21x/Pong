import board

# make board
main = board.core(20, 20)

# while playing update
while main.Active():

    main.Event()
    main.Update()
    main.Render()

# delete object
main.Exit()
