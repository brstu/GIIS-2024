import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.util.ArrayList;

public class AddressBookApp extends JFrame {
    private ArrayList<String> records = new ArrayList<>();
    private int currentRecordIndex = -1;
    private JTextField recordField;
    private JLabel statusLabel;

    public AddressBookApp() {
        super("Address Book");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 200);
        setLayout(new BorderLayout());

        JPanel topPanel = new JPanel();
        recordField = new JTextField(20);
        JButton previousButton = new JButton("Previous");
        JButton nextButton = new JButton("Next");
        topPanel.add(previousButton);
        topPanel.add(recordField);
        topPanel.add(nextButton);

        JPanel bottomPanel = new JPanel();
        JButton addButton = new JButton("Add");
        JButton deleteButton = new JButton("Delete");
        JButton editButton = new JButton("Edit");
        JButton saveButton = new JButton("Save");
        JButton loadButton = new JButton("Load");
        JButton exportButton = new JButton("Export");
        JButton removeButton = new JButton("Remove");
        bottomPanel.add(exportButton);
        bottomPanel.add(removeButton);
        bottomPanel.add(addButton);
        bottomPanel.add(deleteButton);
        bottomPanel.add(editButton);
        bottomPanel.add(saveButton);
        bottomPanel.add(loadButton);

        statusLabel = new JLabel();
        add(topPanel, BorderLayout.NORTH);
        add(bottomPanel, BorderLayout.CENTER);
        add(statusLabel, BorderLayout.SOUTH);

        previousButton.addActionListener(e -> showPreviousRecord());
        nextButton.addActionListener(e -> showNextRecord());
        addButton.addActionListener(e -> addRecord());
        deleteButton.addActionListener(e -> deleteRecord());
        editButton.addActionListener(e -> editRecord());
        saveButton.addActionListener(e -> saveToFile());
        loadButton.addActionListener(e -> loadFromFile());
        exportButton.addActionListener(e -> exportRecord());
        removeButton.addActionListener(e -> removeRecord());

        loadFromFile(); // Load records from file on startup
        showRecord();
    }

    private void showPreviousRecord() {
        if (currentRecordIndex > 0) {
            currentRecordIndex--;
            showRecord();
        }
    }

    private void showNextRecord() {
        if (currentRecordIndex < records.size() - 1) {
            currentRecordIndex++;
            showRecord();
        }
    }

    private void showRecord() {
        if (records.isEmpty()) {
            recordField.setText("");
            statusLabel.setText("No records");
        } else {
            recordField.setText(records.get(currentRecordIndex));
            statusLabel.setText("Record " + (currentRecordIndex + 1) + " of " + records.size());
        }
    }

    private void addRecord() {
        String newRecord = JOptionPane.showInputDialog("Enter new record:");
        if (newRecord != null && !newRecord.isEmpty()) {
            records.add(newRecord);
            currentRecordIndex = records.size() - 1;
            showRecord();
        }
    }

    private void deleteRecord() {
        if (!records.isEmpty()) {
            records.remove(currentRecordIndex);
            if (currentRecordIndex >= records.size()) {
                currentRecordIndex = records.size() - 1;
            }
            showRecord();
        }
    }

    private void editRecord() {
        if (!records.isEmpty()) {
            String editedRecord = JOptionPane.showInputDialog("Edit record:", records.get(currentRecordIndex));
            if (editedRecord != null && !editedRecord.isEmpty()) {
                records.set(currentRecordIndex, editedRecord);
                showRecord();
            }
        }
    }

    private void saveToFile() {
        try (PrintWriter writer = new PrintWriter("address_book.txt")) {
            for (String record : records) {
                writer.println(record);
            }
            statusLabel.setText("Records saved to file");
        } catch (IOException e) {
            statusLabel.setText("Error saving records to file");
        }
    }

    private void loadFromFile() {
        try (BufferedReader reader = new BufferedReader(new FileReader("address_book.txt"))) {
            records.clear();
            String line;
            while ((line = reader.readLine()) != null) {
                records.add(line);
            }
            currentRecordIndex = records.isEmpty() ? -1 : 0;
            showRecord();
            statusLabel.setText("Records loaded from file");
        } catch (IOException e) {
            statusLabel.setText("Error loading records from file");
        }
    }

    private void exportRecord() {
        if (!records.isEmpty()) {
            String filename = "record_" + (currentRecordIndex + 1) + ".txt";
            try (PrintWriter writer = new PrintWriter(filename)) {
                writer.println(records.get(currentRecordIndex));
                statusLabel.setText("Record exported to " + filename);
            } catch (IOException e) {
                statusLabel.setText("Error exporting record");
            }
        }
    }

    private void removeRecord() {
        if (!records.isEmpty()) {
            records.remove(currentRecordIndex);
            if (currentRecordIndex >= records.size()) {
                currentRecordIndex = records.size() - 1;
            }
            showRecord();
            statusLabel.setText("Record removed");
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new AddressBookApp().setVisible(true);
        });
    }
}
