package com.example.lab_4;

import javafx.animation.*;
import javafx.application.Application;
import javafx.application.Preloader;
import javafx.geometry.Bounds;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;


public class HelloApplication extends Application {

    private static final int WIDTH = 1000;
    private static final int HEIGHT = 800;
    private static final double PLAYER_SPEED = 3.5;
    private static final double ENEMY_SPEED = 50;
    private static final double BULLET_SPEED = 4.5;
    private static double ENEMY_BULLET_SPEED = 5.0;
    private static boolean ENEMY_RIGHT = false;
    private static boolean ENEMY_VERTICAL = false;
    private static boolean GAME_OVER = false;
    private static double enemyWidth = 50;
    private static double enemyHeight = 50;
    private static double playerWidth = 50;
    private static double playerHeight = 50;
    private static int NUM_ENEMIES = 15;
    private static int ROW = 4;
    private static int SCORE = 0;
    private static double SPEED_ANIMATION = 1.3;
    private double NUM_SHOTING = 1.7;
    private double CHANGE_SHOOT = 0.6;
    private static double playerX = WIDTH/2;
    private static double playerY = HEIGHT-100;
    private static String[] ENEMY_IMAGIES = new String[]{"file:src/img/enemy_1.png","file:src/img/enemy_2.png",
            "file:src/img/dead_enemy.png"};
    private static Image ImageBackground = new Image("file:src/img/back.jpg");
    private static Image playersImage = new Image("file:src/img/starship.png");
    private static Image bulletImage = new Image("file:src/img/shot_2.png");
    private static ImageView player;
    private List<ImageView> bullets = new ArrayList<>();
    private List<ImageView> enemyBullets = new ArrayList<>();
    private Image enemyBulletImage = new Image("file:src/img/enemy_shot.png");
    private  List<ImageView>[]  enemies = new List[ROW];
    private static boolean SHOOTING = false;
    private static int[][] STATUS_ENEMY = new int[ROW][NUM_ENEMIES];
    private static Timeline animationEnemy;
    private boolean moveLeft = false;
    private boolean moveRight = false;
    private Label score_table;
    private Label textGameOver;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Space Invaders");
        Pane root = new Pane();

        createGUI(root);

        Scene scene = new Scene(root);
        scene.setFill(Color.rgb(31,38,107));

        controllPlayer(scene, root);
        animation(root);

        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private void createGUI(Pane root){
        createLabel(root);
        createUnits(root);
    }
    private void animation( Pane root){
        animationEnemy = new Timeline(new KeyFrame(Duration.millis(2000), e -> moveEnemy(root)));
        animationEnemy.setCycleCount(Animation.INDEFINITE);
        animationEnemy.play();

        Timeline animationPlayer = new Timeline(new KeyFrame(Duration.millis(10), e -> run()));
        animationPlayer.setCycleCount(Animation.INDEFINITE);
        animationPlayer.play();

        Timeline animationBullet = new Timeline(new KeyFrame(Duration.millis(10), e -> moveBullets(root)));
        animationBullet.setCycleCount(Animation.INDEFINITE);
        animationBullet.play();

        Timeline animationEnemyBullet = new Timeline(new KeyFrame(Duration.millis(10), e -> moveEnemyBullets(root)));
        animationEnemyBullet.setCycleCount(Animation.INDEFINITE);
        animationEnemyBullet.play();

        new AnimationTimer() {
            @Override
            public void handle(long now) {
                if (GAME_OVER) {
                    animationEnemy.stop();
                    animationPlayer.stop();
                    textGameOver.setVisible(true);
                    root.getChildren().remove(player);
                    for (int i = 0; i < ROW; i++){
                        Iterator<ImageView> enemyIterator = enemies[i].iterator();
                        while(enemyIterator.hasNext()){
                            ImageView enemy = enemyIterator.next();
                            root.getChildren().remove(enemy);
                            enemyIterator.remove();
                            enemies[i].remove(enemy);
                        }
                    }
                }
            }
        }.start();

    }
    private void controllPlayer(Scene scene, Pane root){
        scene.setOnKeyPressed(event -> {
            if (event.getCode() == KeyCode.LEFT) {
                moveLeft = true;
            } else if (event.getCode() == KeyCode.RIGHT) {
                moveRight = true;
            }
            if (event.getCode() == KeyCode.SPACE && SHOOTING && !GAME_OVER ){
                toShooting(root);
                SHOOTING = false;
            }
        });

        scene.setOnKeyReleased(event -> {
            if (event.getCode() == KeyCode.LEFT) {
                moveLeft = false;
            } else if (event.getCode() == KeyCode.RIGHT) {
                moveRight = false;
            }
            if (event.getCode() == KeyCode.SPACE && !SHOOTING ){
                SHOOTING=true;
            }
        });
    }

    private void createLabel(Pane root){
        ImageView ImageBackgroundView = new ImageView(ImageBackground);
        ImageBackgroundView.setFitWidth(WIDTH);
        ImageBackgroundView.setFitHeight(HEIGHT);
        root.getChildren().add(ImageBackgroundView);

        String formatScore = String.format("Score: %04d", SCORE);
        score_table = new Label(formatScore);
        score_table.setFont(Font.font("Aria", FontWeight.BOLD, 25));
        score_table.setTextFill(Color.WHITE);
        score_table.setLayoutY(30);
        score_table.setLayoutX(825);
        root.getChildren().add(score_table);


        textGameOver = new Label("Game Over");
        textGameOver.setFont(Font.font("Aria", FontWeight.BOLD, 60));
        textGameOver.setTextFill(Color.RED);
        textGameOver.setLayoutY(HEIGHT/2-50);
        textGameOver.setLayoutX(WIDTH/2-150);
        textGameOver.setVisible(false);
        root.getChildren().add(textGameOver);

        Canvas canvas = new Canvas(WIDTH, HEIGHT);
        root.getChildren().add(canvas);
    }
    private void createUnits(Pane root){
        createPlayer(root);
        createEnemy(root);
    }

    private void createPlayer(Pane root){
        player = new ImageView(playersImage);
        player.setFitWidth(playerWidth);
        player.setFitHeight(playerHeight);
        player.setX(playerX);
        player.setY(playerY);
        root.getChildren().add(player);
    }
    private void createEnemy(Pane root){
        for(int i = 0; i< ROW; i++){
            enemies[i] = new ArrayList<>();
            for(int j = 0; j < NUM_ENEMIES; j ++){
                if (Math.random()>0.5)
                {
                    STATUS_ENEMY[i][j]=1;
                } else{
                    STATUS_ENEMY[i][j]=0;
                }
                ImageView enemy = new ImageView(new Image(ENEMY_IMAGIES[STATUS_ENEMY[i][j]]));
                enemy.setFitHeight(enemyHeight);
                enemy.setFitWidth(enemyWidth);
                enemy.setX(100+j*60);
                enemy.setY(100+ enemyWidth * 1.2 * i);
                root.getChildren().add(enemy);
                enemies[i].add(enemy);
            }
        }
    }
    private void moveEnemy(Pane root){
        boolean isChange = false;
        int shots_taken = 0;
        for (int i = 0; i < ROW; i++){
            if(!enemies[i].isEmpty()){
                double rightPosition = enemies[i].getLast().getX()+ enemyWidth;
                double leftPosition = enemies[i].getFirst().getX();
                if (ENEMY_RIGHT && rightPosition + enemyWidth > WIDTH && !isChange ){
                    ENEMY_RIGHT = false;
                    ENEMY_VERTICAL = true;
                    isChange =true;
                } else if(!ENEMY_RIGHT && leftPosition - enemyWidth/2 <= 0 && !isChange){
                    ENEMY_RIGHT = true;
                    ENEMY_VERTICAL = true;
                    isChange =true;
                }
                int index = 0;
                double directionHorizontal = ENEMY_RIGHT ? ENEMY_SPEED: -ENEMY_SPEED;
                double directionVertical = ENEMY_VERTICAL ? enemyHeight/2: 0;
                for (ImageView enemy: enemies[i]){
                    STATUS_ENEMY[i][index]= (STATUS_ENEMY[i][index]+1)%2;
                    if(Math.random()>CHANGE_SHOOT && shots_taken<NUM_SHOTING){
                        enemyShooting(root, enemy);
                        shots_taken++;
                    }
                    if (enemy.getY()+enemyHeight+directionVertical >= HEIGHT){
                        GAME_OVER=true;
                        break;
                    }
                    enemy.setImage(new Image(ENEMY_IMAGIES[STATUS_ENEMY[i][index]]));
                    enemy.setX(enemy.getX()+directionHorizontal);
                    enemy.setY(enemy.getY()+directionVertical);
                    index++;
                }

            }
        }
        ENEMY_VERTICAL = false;
    }
    private void run(){
        double deltaX = 0;

        if (moveLeft) {
            deltaX -= PLAYER_SPEED;
        }
        if (moveRight) {
            deltaX += PLAYER_SPEED;
        }
        movePlayer(deltaX);
    }

    private void movePlayer(double deltaX) {
        if (player.getX() +deltaX >0 && player.getX() + playerWidth + deltaX <WIDTH){
            player.setX(player.getX()+deltaX);
        }
    }

    private void enemyShooting(Pane root, ImageView enemy){
        ImageView  bullet = new ImageView(enemyBulletImage);

        bullet.setFitWidth(8);
        bullet.setFitHeight(70);

        bullet.setX(enemy.getX()+ enemy.getFitHeight()/2 - bullet.getFitWidth()/2);
        bullet.setY(enemy.getY() + bullet.getFitHeight());

        root.getChildren().add(bullet);
        enemyBullets.add(bullet);

    }

    private void toShooting (Pane root){
        ImageView bullet = new ImageView(bulletImage);

        bullet.setFitWidth(5);
        bullet.setFitHeight(30);

        bullet.setX(player.getX()+ player.getFitHeight()/2 - bullet.getFitWidth()/2);
        bullet.setY(player.getY()-bullet.getFitHeight());

        root.getChildren().add(bullet);
        bullets.add(bullet);
    }
    private void moveEnemyBullets(Pane root){
        List<ImageView> bulletsToRemove = new ArrayList<>();

        for(ImageView bullet: enemyBullets){
            bullet.setY(bullet.getY()+ENEMY_BULLET_SPEED);
            if (bullet.getY()+bullet.getFitHeight()>HEIGHT){
                bulletsToRemove.add(bullet);

            }
        }

        for(ImageView bullet: enemyBullets){
            Bounds playerBounds = player.getBoundsInParent();
            Bounds bulletBounds = bullet.getBoundsInParent();
            if (bulletBounds.intersects(playerBounds)){
                bulletsToRemove.add(bullet);
                GAME_OVER = true;
            }
        }
        Iterator<ImageView> bulletIterator = bulletsToRemove.iterator();
        while(bulletIterator.hasNext()){
            ImageView bullet = bulletIterator.next();
            root.getChildren().remove(bullet);
            bulletIterator.remove();
            for (int i = 0; i < ROW; i++){
                enemies[i].remove(bullet);
            }

        }

    }
    private void moveBullets(Pane root){
        List<ImageView> bulletsToRemove = new ArrayList<>();

        for (ImageView bullet: bullets){
            bullet.setY(bullet.getY()- BULLET_SPEED);

            if (bullet.getY()<0){
                bulletsToRemove.add(bullet);
            }
        }
        List<ImageView> enemiesToRemove = new ArrayList<>();
        for (int i = 0; i < ROW; i++ ){
            for(ImageView enemy: enemies[i]){
                for(ImageView bullet: bullets){
                    Bounds enemyBounds = enemy.getBoundsInParent();
                    Bounds bulletBounds = bullet.getBoundsInParent();
                    if(bulletBounds.intersects(enemyBounds))
                    {
                        if(i == 0){
                            CHANGE_SHOOT +=CHANGE_SHOOT*0.03;
                            System.out.printf(String.valueOf(CHANGE_SHOOT));
                            NUM_SHOTING*=1.1;
                            animationEnemy.setRate(SPEED_ANIMATION);
                        }
                        bulletsToRemove.add(bullet);
                        enemiesToRemove.add(enemy);
                        SCORE+=30;
                        String formatScore = String.format("Score: %04d", SCORE);
                        score_table.setText(formatScore);
                    }
                }
            }
        }

        Iterator<ImageView> enemyIterator = enemiesToRemove.iterator();
        while(enemyIterator.hasNext()){
            ImageView enemy = enemyIterator.next();
            root.getChildren().remove(enemy);
            enemyIterator.remove();
            for (int i = 0; i < ROW; i++){
                enemies[i].remove(enemy);
            }

        }
        for(ImageView bullet : bulletsToRemove){
            root.getChildren().remove(bullet);
            bullets.remove(bullet);
        }
    }
}
