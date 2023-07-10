resource "kubernetes_service" "frontend_svc" {
  metadata {
    namespace = data.kubernetes_namespace.default.metadata.0.name
    name      = local.base_name
  }
  spec {
    type     = "ClusterIP"
    selector = local.selectors
    port {
      port        = 8080
      protocol    = "TCP"
      name        = "http"
      target_port = 8080
    }
  }
}
