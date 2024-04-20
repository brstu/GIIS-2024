def handle_game_over_events(game_over_flag):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if game_over_flag:
                    pygame.mixer.music.play(-1)
                    reset_game()
                    game_over_flag = False
                else:
                    jump()