package org.example;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.HashMap;
import java.util.Map;

public class Main {

    private static JPanel panel;
    private static JFrame frame;
    private static JTextField nameField;
    private static JTextArea allContactsText;
    private static JTextArea addressArea;
    private static HashMap<String, String> information;

    public static void main(String[] arg) {
        information = new HashMap<>();
        SwingUtilities.invokeLater(Main::createAndShowGUI);
    }

    private static void createAndShowGUI() {
        panel = new JPanel(null);
        addComponents();
        setFrameProperties();
    }

    private static void addComponents() {
        addButtons();
        addLabelsAndFields();
    }

    private static void addButtons() {
        addButton("Add", 800, 10, 100, 25, (e) -> addContact());
        addButton("Edit", 800, 60, 100, 25, (e) -> editContact());
        addButton("Remove", 800, 110, 100, 25, (e) -> removeContact());
        addButton("Find", 800, 160, 100, 25, (e) -> findContact());
        addButton("Load", 800, 210, 100, 25, (e) -> loadContactsFromFile());
        addButton("Save", 800, 260, 100, 25, (e) -> saveContactsToFile());
        addButton("Next", 500, 650, 300, 30, (e) -> nextContact());
        addButton("Previous", 200, 650, 300, 30, (e) -> previousContact());
    }



    private static void addButton(String text, int x, int y, int width, int height, ActionListener actionListener) {
        JButton button = new JButton(text);
        button.setBackground(Color.green);
        button.setBounds(x, y, width, height);
        button.addActionListener(actionListener);
        panel.add(button);
    }

    private static void addLabelsAndFields() {
        addLabel("Name:", 10, 10, 50, 20);
        addLabel("Address:", 10, 50, 50, 20);
        nameField = new JTextField("", 1);
        nameField.setFocusable(false);
        nameField.setBounds(70, 10, 200, 20);
        panel.add(nameField);
        addressArea = new JTextArea();
        addressArea.setLineWrap(true);
        JScrollPane jScrollPane = new JScrollPane(addressArea);
        jScrollPane.setBounds(70, 50, 200, 200);
        panel.add(jScrollPane);
        JLabel allContactsLabel = new JLabel("All Contacts:");
        allContactsLabel.setBounds(300, 10, 100, 20);
        panel.add(allContactsLabel);
        allContactsText = new JTextArea();
        allContactsText.setLineWrap(true);
        allContactsText.setFocusable(false);
        JScrollPane scrollPaneOfAllContacts = new JScrollPane(allContactsText);
        scrollPaneOfAllContacts.setBounds(380, 10, 400, 400);
        panel.add(scrollPaneOfAllContacts);
    }

    private static void addLabel(String text, int x, int y, int width, int height) {
        JLabel label = new JLabel(text);
        label.setBounds(x, y, width, height);
        panel.add(label);
    }

    private static void setFrameProperties() {
        frame = new JFrame("Адрессная книга");
        frame.setSize(1000, 800);
        frame.setVisible(true);
        frame.setLayout(null);
        frame.setLocationRelativeTo(null);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(panel);
    }

    private static void addContact() {
        JPanel panel = new JPanel(new GridLayout(2, 2));
        JLabel label1 = new JLabel("Имя:");
        JTextField nameTextField = new JTextField("");
        JLabel label2 = new JLabel("Адрес:");
        JTextArea addressArea = new JTextArea();
        panel.add(label1);
        panel.add(nameTextField);
        panel.add(label2);
        panel.add(addressArea);
        int option = JOptionPane.showOptionDialog(null, panel, "Введите данные", JOptionPane.OK_CANCEL_OPTION,
                JOptionPane.PLAIN_MESSAGE, null, null, null);
        if (option == JOptionPane.OK_OPTION) {
            if(nameTextField.getText().isEmpty() || addressArea.getText().isEmpty() ){
                JOptionPane.showMessageDialog(null, "Enter all the data", "Error", JOptionPane.ERROR_MESSAGE);
            }else {
                if(information.containsKey(nameTextField.getText())){
                    JOptionPane.showMessageDialog(null, "The contact already exists", "Error", JOptionPane.ERROR_MESSAGE);
                }else {
                    information.put(nameTextField.getText(), addressArea.getText());
                    JOptionPane.showMessageDialog(null, "Contact added", "Succes", JOptionPane.PLAIN_MESSAGE);
                    viewAllContacts();
                }
            }
        }
    }

    private static void editContact() {
        information.put(nameField.getText(), addressArea.getText());
        viewAllContacts();
    }

    private static void removeContact() {
        int option = JOptionPane.showConfirmDialog(null, "Вы уверены, что хотите удалить контакт ?", "Подтверждение",  JOptionPane.OK_CANCEL_OPTION);
        if (option == JOptionPane.YES_OPTION){
            information.remove(nameField.getText());
            nameField.setText("");
            addressArea.setText("");
            viewAllContacts();
        }
    }

    public static void findContact() {
        String input = JOptionPane.showInputDialog(null, "Enter name:", "Enter data", JOptionPane.PLAIN_MESSAGE);
        if(information.containsKey(input)){
            nameField.setText(input);
            addressArea.setText(information.get(input));
        }else{
            JOptionPane.showMessageDialog(null, "Пользователь не найден", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private static void loadContactsFromFile() {
        JFileChooser fileChooser = new JFileChooser();
        int result = fileChooser.showSaveDialog(frame);
        if (result == JFileChooser.APPROVE_OPTION){
            try {
                String filePath = fileChooser.getSelectedFile().getAbsolutePath();
                BufferedReader reader = new BufferedReader(new FileReader(filePath));
                String line;
                information.clear();
                while ((line = reader.readLine()) != null) {
                    String key = line.substring(0, line.indexOf(" "));
                    String value = line.substring(line.indexOf(" ") + 1, line.length() - 1);
                    information.put(key, value);
                }
            } catch (FileNotFoundException ex) {
                throw new IllegalArgumentException("File not found", ex);
            } catch (IOException ex) {
                throw new IllegalStateException("Error reading file", ex);
            }
            viewAllContacts();
        }
    }


    private static void saveContactsToFile() {
        JFileChooser fileChooser = new JFileChooser();
        int result = fileChooser.showSaveDialog(frame);

        if (result == JFileChooser.APPROVE_OPTION) {
            String filePath = fileChooser.getSelectedFile().getAbsolutePath();

            try (FileWriter writer = new FileWriter(filePath)) {
                information.forEach((k, v) -> {
                    try {
                        writer.write(k + " " + v + "\n");
                    } catch (IOException ex) {
                        ex.printStackTrace(); // Обработка исключения (здесь просто выводим сообщение об ошибке)
                    }
                });
            } catch (IOException ex) {
                ex.printStackTrace(); // Обработка исключения (здесь просто выводим сообщение об ошибке)
            }
        }
    }

    private static void nextContact() {
        boolean check = false;
        for (Map.Entry<String, String> entry: information.entrySet()){
            if (check){
                nameField.setText(entry.getKey());
                addressArea.setText(entry.getValue());
                break;
            } else if(!check && entry.getValue() == information.get(nameField.getText())){
                check = true;
            }

        }
    }

    private static void previousContact() {
        boolean check = false;
        String key = null;
        for (Map.Entry<String, String> entry: information.entrySet()){
            if(!check && entry.getValue() == information.get(nameField.getText()) && key!= null){
                check = true;
                nameField.setText(key);
                addressArea.setText(information.get(key));
                break;
            }
            key = entry.getKey();
        }
    }
    private static void viewAllContacts() {
        StringBuilder text = new StringBuilder();
        for (Map.Entry<String, String> entry : information.entrySet()) {
            text.append(" ").append(entry.getKey()).append("\t").append(entry.getValue()).append("\n");
        }
        allContactsText.setText(text.toString());
    }
}
