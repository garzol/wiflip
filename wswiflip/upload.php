<?php
// upload.php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  http_response_code(405);
  echo json_encode(['ok' => false, 'error' => 'POST only']);
  exit;
}

if (!isset($_FILES['files'])) {
  http_response_code(400);
  echo json_encode(['ok' => false, 'error' => 'No files uploaded']);
  exit;
}

// Ensure upload dir exists
$uploadDir = __DIR__ . '/uploads';
if (!is_dir($uploadDir)) {
  mkdir($uploadDir, 0775, true);
}

$files = $_FILES['files'];
$count = is_array($files['name']) ? count($files['name']) : 1;

$results = [];

for ($i = 0; $i < $count; $i++) {
  $name = is_array($files['name']) ? $files['name'][$i] : $files['name'];
  $tmp  = is_array($files['tmp_name']) ? $files['tmp_name'][$i] : $files['tmp_name'];
  $type = is_array($files['type']) ? $files['type'][$i] : $files['type'];
  $size = is_array($files['size']) ? $files['size'][$i] : $files['size'];

  if (!is_uploaded_file($tmp)) {
    $results[] = ['ok' => false, 'name' => $name, 'error' => 'Upload failed'];
    continue;
  }

  // Simple filename sanitization
  $safeName = preg_replace('/[^A-Za-z0-9._-]/', '_', $name);
  $target = $uploadDir . '/' . uniqid('upload_', true) . '_' . $safeName;

  if (move_uploaded_file($tmp, $target)) {
    $results[] = [
      'ok' => true,
      'name' => $name,
      'type' => $type,
      'size' => $size,
      'savedAs' => basename($target),
    ];
  } else {
    $results[] = ['ok' => false, 'name' => $name, 'error' => 'Could not move file'];
  }
}

echo json_encode(['ok' => true, 'count' => count($results), 'files' => $results]);
